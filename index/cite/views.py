# Create your views here.
from django.http import Http404, HttpResponse

def hello(request, path):
    return HttpResponse("Hello world at %s" % (path) )
