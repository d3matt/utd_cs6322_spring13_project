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

    ('^$', hello, None),
    ('^author$', author_list, None),
    ('^author/\d+$', author_detail, None),
    ('^paper$', paper_list, None),
    ('^paper/\d+$', paper_detail, None),
    ('^paper/json/\d+$', paper_json, None),
    ('^token/\d+$', token_lookup, None),

)
