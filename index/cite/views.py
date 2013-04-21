from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response

from cite.models import Author, Paper, Token

def hello(request):
    len1 = Paper.objects.count()
    len2 = Author.objects.count()
    len3 = Token.objects.count()
    return render_to_response('frontpage.html', {'len1': len1, 'len2': len2, 'len3': len3})


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
