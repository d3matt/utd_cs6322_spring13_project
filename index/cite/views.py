import json
import os
import time
import xml.dom.minidom

from math import log,sqrt
from tempfile import mkstemp

from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response

from cite.forms import TopicSearchForm
from cite.models import Author, Paper, Token, PaperToken
from cite.utils import SortedList

def hello(request):
    len1 = Paper.objects.count()
    len2 = Author.objects.count()
    len3 = Token.objects.count()

    cite_list = SortedList(max_length=10)
    rcite_list = SortedList(max_length=10)

    #this would generate the list dynamically...
    #papers = Paper.objects.all()
    #for paper in papers:
    #    count = 0
    #    for p in Paper.objects.filter(citations__id__exact=paper.id):
    #        count += 1
    #    rcite_list.insert(paper, count)
    for id_ in [ 777, 658, 889, 304, 878, 7451, 576, 905, 9594, 2041]:
        paper = Paper.objects.get(id=id_)
        count = 0
        for p in Paper.objects.filter(citations__id__exact=paper.id):
            count += 1
        rcite_list.insert(paper, count)
    for id_ in [ 2485, 7677, 47367, 8097, 1345, 4227, 1017, 65899, 3657, 6024 ]:
        paper = Paper.objects.get(id=id_)
        cite_list.insert(paper, paper.citations.count())
    return render_to_response('frontpage.html', {'len1': len1,
                'len2': len2,
                'len3': len3,
                'cite_list': cite_list,
                'rcite_list': rcite_list,
                })


def author_list(request):
    author_list = Author.objects.all()
    return render_to_response('author_list.html', {'author_list': author_list})


def paper_list(request):
    paper_list = Paper.objects.all()
    return render_to_response('paper_list.html', {'paper_list': paper_list})


def author_detail(request, author_id):
    author = Author.objects.get(id=author_id)
    return render_to_response('author_detail.html', {'author' : author})


def paper_detail(request, paper_id):
    paper = Paper.objects.get(id=paper_id)
    token_list = paper.papertoken_set.all()
    common_tokens = sorted(token_list, key=lambda token: token.num, reverse=True)[0:5]

    rcitations = []
    for p in Paper.objects.filter(citations__id__exact=paper.id):
        rcitations.append(p)
    
    uncommon_ = []
    for token in token_list:
        if token.num < 5:
            uncommon_.append(token)
    uncommon_tokens = sorted(uncommon_, key=lambda token: token.num)

    return render_to_response('paper_detail.html', {'paper': paper,
                    'common_tokens': common_tokens,
                    'uncommon_tokens': uncommon_tokens,
                    'rcitations': rcitations
                    })


def token_lookup(request, token_id):
    token = Token.objects.get(id=token_id)
    papers = []
    papertokens = token.papertoken_set.all()
    for pt in papertokens:
        papers.append(pt.paper)
    return render_to_response('token_lookup.html', {'token': token, 'papers': papers})


def add_node(p, nodes, retval, size=0):
    """adds a node to the graph"""
    if p.id not in nodes:
        nodes[p.id] = len(nodes)
        retval["nodes"].append({"id": str(p.id), "title": p.title, "size": size})


def dfs_paper(p, nodes, edges, retval, max_level=1):
    """does a depth first search (up to the max depth specified) starting at node p"""
    for cite in p.citations.all():
        add_node(cite, nodes, retval)
        if max_level > 0 :
            dfs_paper(cite, nodes, edges, retval, max_level-1)
        if (p.id,cite.id) not in edges:
            edges.append( (p.id,cite.id) )
    for rcite in Paper.objects.filter(citations__id__exact=p.id):
        add_node(rcite, nodes, retval)
        if max_level > 0 :
            dfs_paper(rcite, nodes, edges, retval, max_level-1)
        if (rcite.id, p.id) not in edges:
            edges.append( (rcite.id, p.id) )


def paper_json(request, paper_id):
    paper = Paper.objects.get(id=paper_id)
    response = HttpResponse(content_type='text/json; charset=utf-8')

    retval = {}
    retval["directed"] = True
    retval["mulitgraph"] = False
    retval["graph"] = []
    retval["nodes"] = []
    retval["links"] = []
    nodes = {}
    edges = []

    add_node(paper, nodes, retval, 20)
    dfs_paper(paper, nodes, edges, retval, 1)
    #convert edges to format expected by D3
    for f,t in edges:
        retval["links"].append( { "source" : nodes[f], "target" : nodes[t]} )

    #for legible json for debugging
    indent = 0
    try:
        if "indent" in request.POST:
            indent=int(request.POST["indent"])
        if "indent" in request.GET:
            indent=int(request.GET["indent"])
    except:
        pass

    if indent > 0:
        response.write(json.dumps(retval, indent=indent))
    else:
        response.write(json.dumps(retval))
    return response

#third party stemmer
import porter
def stem(word):
    stem = porter.PorterStemmer().stem
    return stem(word, 0,len(word)-1)

STOP_WORDS = []
def load_stopwords():
    f = open( os.path.abspath(os.path.dirname(__file__)) +
        "/../../cite/HeaderParseService/resources/database/stopwords")
    for line in f:
        word = line.strip()
        if word:
            STOP_WORDS.append(word)
load_stopwords()

def log_text(text, request):
    f = open("queries.log", 'a')
    f.write(time.strftime("%c") + " from " + request.META["REMOTE_ADDR"] + "\n")
    f.write(text)
    f.write("\n\n")

def topic_graph(text, request):
    log_text(text, request)
    data = {}
    data["directed"] = True
    data["mulitgraph"] = False
    data["graph"] = []
    data["nodes"] = []
    data["links"] = []
    topics = {}
    nodes = {}
    for line in text.splitlines():
        words = line.split()
        topic = words[0].lower()
        d = {}
        topics[topic] = d
        d["orig"] = words
        d["tokens"] = set()
        d["Tokens"] = [] #actual Token objects (gotta do the DB lookup anyway)
        d["papers"] = set()
        nodes[topic] = len(nodes)
        for word in words:
            word = word.lower()
            token = stem(word)
            if word not in STOP_WORDS and token not in STOP_WORDS:
                d["tokens"].add(token)
        for token in d["tokens"]:
            try:
                t = Token.objects.get(stem=token)
            except:
                continue
            d["Tokens"].append(t)
            l = PaperToken.objects.filter(token=t)
            for pt in l:
                d["papers"].add(pt.paper_id)
        size = len(d["papers"])
        if size:
            size = log(size, 2)
        data["nodes"].append({"id": topic, "title": topic, "size": size })

    for i in topics:
        for j in topics:
            if i is j:
                continue
            p1 = topics[i]["papers"]
            p2 = topics[j]["papers"]
            inter = p1.intersection(p2)
            if len(inter) > 0:
                src = nodes[i]
                dst = nodes[j]
                width = log(len(inter),2)
                data["links"].append({"source": src, "target": dst, "width": width})

    return render_to_response('topic_search_results.html', {'json_data': json.dumps(data), 'topics': topics})

def topic_search(request):
    if request.POST:
        form = TopicSearchForm(request.POST)
        if form.is_valid():
            return topic_graph(form.cleaned_data["block"], request)
    else:
        #provide a nice initial graph
        initial = {'block': """chinese pizza
english nouns
semantics computation
""", }
        form = TopicSearchForm(initial = initial)
    return render_to_response('topic_search_form.html', {'form': form})
