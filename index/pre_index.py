import json
import os
import re
import xml.dom.minidom
from xml.dom.minidom import parse, parseString


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "index.settings")
from cite.models import *


#this is VERY VERY DANGEROUS...  do not run pre_index while django is running!
from django.db import connection
cursor = connection.cursor()
cursor.execute('PRAGMA temp_store = MEMORY;')
cursor.execute('PRAGMA synchronous=OFF')


#third party stemmer
import porter
def stem(word):
    stem = porter.PorterStemmer().stem
    return stem(word, 0,len(word)-1)

class InvalidXml(Exception):
    pass

def parse_cxml(filename):
    dom = parse(filename + ".cxml")
    citations = []
    for citation in dom.getElementsByTagName("citation"):
        attrs = citation.attributes
        if (not attrs.has_key('valid')) or (attrs.get('valid').value != 'true'):
            continue
        cite = parse_citation(citation)
        if cite:
            citations.append(cite)
    return citations

def parse_citation(node):
    simple_element_list = ["title"]
    ignore_element_list = [ "date", "title", "booktitle", "pages", "location",
                            "marker", "journal", "rawString", "contexts",
                            "volume", "institution", "tech", "publisher",
                            "editor", "note",
                            ]
    retval = {}
    for child in node.childNodes:
        if not isinstance(child, xml.dom.minidom.Element):
            continue

        if child.nodeName in simple_element_list:
            retval[child.nodeName] = child.childNodes[0].data
        elif child.nodeName in ignore_element_list:
            #don't know, don't care...
            pass
        elif child.nodeName == "authors":
            retval["authors"] = []
            for author in child.childNodes:
                if not isinstance(author, xml.dom.minidom.Element):
                    continue
                achild = author.childNodes[0]
                if not isinstance(achild, xml.dom.minidom.Text):
                    raise InvalidXml()
                retval["authors"].append(achild.data)
        else:
            print "\tunknown field:", child.nodeName
    if "title" not in retval:
        return None
    return retval

def parse_hxml(filename):
    retval = {}
    dom = parse(filename + ".hxml")    
    title = dom.getElementsByTagName("title")[0].childNodes[0].data.strip()
    authors = []
    for node in dom.getElementsByTagName("author"):
        for child in node.childNodes:
            if not isinstance(child, xml.dom.minidom.Element):
                continue
            if child.nodeName == "name":
                authors.append(child.childNodes[0].data.strip())
    return (title, authors)


STOP_WORDS = []
def load_stopwords():
    f = open( os.path.abspath(os.path.dirname(__file__)) +
        "/../cite/HeaderParseService/resources/database/stopwords")
    for line in f:
        word = line.strip()
        if word:
            STOP_WORDS.append(word)
load_stopwords()

def parse_txt(filename):
    """returns (length, stem:num_words) dict, mostly ripped from Matthew Stoltenberg's HW 1/2/3"""
    words = open(filename + ".txt").read().split()
    retval = {}
    length = 0
    for word in words:
        orig = word
        word = word.lower().strip()
        #don't count whitespace
        if len(word) == 0:
            continue
        #deal with digits
        elif re.search("\d", word):
            #if any alphabetical characters, do more:
            if re.search("[a-zA-Z]", word):
                word = re.sub("\d", "", word)
                words.append(word)
            continue
        #deal with other characters
        elif re.search("\W", word):
            #allow possesives and contractions
            if re.search("'s$", word):
                pass
            else:
                for w in re.split("\W", word):
                    words.append(w)
                continue
        length += 1
        if word in STOP_WORDS or len(word) == 1:
            continue

        #stem the word
        word = stem(word)
        if word in retval:
            retval[word] += 1
        else:
            retval[word] = 1

    return (length, retval)


def add_or_find_paper(title, length=0):
    l = Paper.objects.filter(title=title)
    if len(l) == 0:
        paper = Paper(title=title, length=length)
        paper.save()
    else:
        paper = l[0]
        if length and paper.length != length:
            paper.length = length
            paper.save()
    return paper

def add_or_find_author(name):
    l = Author.objects.filter(name=name)
    if len(l) == 0:
        author = Author(name=name)
        author.save()
    else:
        author = l[0]
    return author

def add_author(paper, name):
    paper.authors.add(add_or_find_author(name))
    paper.save()

def add_citations(paper, citations):
    for cite in citations:
        t = cite["title"]
        c = add_or_find_paper(t)
        if "authors" in cite:
            for author in cite["authors"]:
                add_author(c, author)
        paper.citations.add(c)

def add_or_find_token_and_add(stem, num):
    l = Token.objects.filter(stem=stem)
    if len(l) == 0:
        token = Token(stem=stem, total=num)
        token.save()
    else:
        token = l[0]
        token.total += num
        token.save()
    return token

def add_token_num(paper, stem, num):
    token = add_or_find_token_and_add(stem, num)
    l = PaperToken.objects.filter(paper=paper, token=token)
    if len(l) == 0:
        t = PaperToken(num=num, paper=paper, token=token)
        t.save()
    else:
        t = l[0]
        t.num=num
        t.save()
    paper.save()

def parse_doc(filename):
    """parses the header xml, citation xml, and txt for the given pdf
assumes everything is valid"""

    l = Paper.objects.filter(filename=filename)
    if len(l) != 0:
        print "Already fully parsed: " + filename
        return
    try:
        title, authors = parse_hxml(filename)
        l = Paper.objects.filter(title=title)
        if len(l) != 0 and paper.filename is not None and paper.filename != filename:
            print "WARNING: %s.pdf and %s.pdf have same title: '%s'" % (filename, paper.filename, title)
            return 

        citations = parse_cxml(filename)
        length, index = parse_txt(filename)
        print filename, title, length
    except:
        print "WARNING: %s.pdf failed to parse" % (filename)
        return 
        

    paper = add_or_find_paper(title, length)
    if paper.filename is not None:
        if paper.filename != filename:
            print "WARNING: %s.pdf and %s.pdf have same title: '%s'" % (filename, paper.filename, title)
            return 
        print "Already fully parsed: " + filename
        return
    for author in authors:
        add_author(paper, author)
    add_citations(paper, citations)

    for stem, num in index.iteritems():
        add_token_num(paper, stem, num)

    paper.filename = filename
    paper.save()

def walk_call(notused, dirname, files):
    for pdf in files:
        if '.pdf' not in pdf:
            continue
        path = dirname + '/' + pdf.replace('.pdf', '')
        missing = False
        for ext in ['.txt', '.cxml', '.hxml', '.check']:
            if not os.path.exists(path + ext):
                print path + ext + " missing! SKIPPING!"
                missing = True
                break
        if missing:
            continue
        check = open(path + '.check').read().strip()
        if check != "document passed filtration" :
            print path + ".txt failed filtration! SKIPPING!"
            continue
        print dirname + "/" + pdf
        parse_doc(path)

if __name__ == "__main__":
    os.path.walk("anthology-new", walk_call, None)
