import json
import os
import re
import xml.dom.minidom
from xml.dom.minidom import parse, parseString


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "index.settings")
import cite.models


#third party stemmer
import porter
def stem(word):
    return stem.stem(word, 0,len(word)-1)
stem.stem = porter.PorterStemmer().stem

class InvalidXml(Exception):
    pass

def parse_cxml(filename):
    dom = parse(filename + ".cxml")
    citations = []
    for citation in dom.getElementsByTagName("citation"):
        attrs = citation.attributes
        if (not attrs.has_key('valid')) or (attrs.get('valid').value != 'true'):
            continue

        citations.append(parse_citation(citation))
    return citations

def parse_citation(node):
    simple_element_list = ["title"]
    ignore_element_list = [ "date",
                            "title",
                            "booktitle",
                            "pages",
                            "location",
                            "marker",
                            "journal",
                            "rawString",
                            "contexts",
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
            print "\t", child.nodeName
    return retval

def parse_hxml(filename):
    retval = {}
    dom = parse(filename + ".hxml")    
    title = dom.getElementsByTagName("title")[0].childNodes[0].data
    authors = []
    for node in dom.getElementsByTagName("author"):
        for child in node.childNodes:
            if not isinstance(child, xml.dom.minidom.Element):
                continue
            if child.nodeName == "name":
                authors.append(child.childNodes[0].data)
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

def parse_doc(filename):
    title, authors = parse_hxml(filename)
    citations = parse_cxml(filename)
    length, index = parse_txt(filename)
    print title, length
    print authors
    print json.dumps(citations, indent=2)
    print index


parse_doc("Y12-1005")
