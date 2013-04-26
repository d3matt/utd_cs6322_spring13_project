from django.conf.urls import patterns, include, url
from cite.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'index.views.home', name='home'),
    # url(r'^index/', include('index.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    ('^$', hello),
    ('^author$', author_list),
    ('^author/(?P<author_id>\d*)$', author_detail),
    ('^paper$', paper_list, None),
    ('^paper/(?P<paper_id>\d*)$', paper_detail),
    ('^paper/json/(?P<paper_id>\d*)$', paper_json),
    ('^token/(?P<token_id>\d*)$', token_lookup),
    ('^search$', topic_search),

)
