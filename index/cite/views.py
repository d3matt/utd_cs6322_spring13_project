import json
import os
import pydot
import xml.dom.minidom
from tempfile import mkstemp

from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response

from cite.models import Author, Paper, Token
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

def author_detail(request):
    id_ = request.get_full_path().split('/')[2]
    author = Author.objects.get(id=id_)
    return render_to_response('author_detail.html', {'author' : author})

def paper_detail(request):
    id_ = request.get_full_path().split('/')[2]
    paper = Paper.objects.get(id=id_)
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

def token_lookup(request):
    id_ = request.get_full_path().split('/')[2]
    token = Token.objects.get(id=id_)
    papers = []
    papertokens = token.papertoken_set.all()
    for pt in papertokens:
        papers.append(pt.paper)
    return render_to_response('token_lookup.html', {'token': token, 'papers': papers})


def paper_json(request):
    id_ = request.get_full_path().split('/')[3]
    paper = Paper.objects.get(id=id_)
    response = HttpResponse(content_type='text/json; charset=utf-8')

    retval = {}
    retval["directed"] = True
    retval["mulitgraph"] = False
    retval["graph"] = []
    retval["nodes"] = []
    nodes = {}
    n = 0
    nodes[paper.id] = n
    n += 1
    retval["nodes"].append( { "id" : str(paper.id), "title": paper.title, "size" : 20, "hovered" : True} )
    retval["links"] = []
    for cite in paper.citations.all():
        if cite.id not in nodes:
            nodes[cite.id] = n
            n += 1
        retval["nodes"].append( { "id" : str(cite.id), "title": cite.title, "size" : 0, "hovered" : False} )
        retval["links"].append( { "source" : nodes[paper.id], "target" : nodes[cite.id]} )


    response.write(json.dumps(retval,indent=2))
    return response
