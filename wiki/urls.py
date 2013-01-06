from django.conf.urls import patterns, url

urlpatterns = patterns('mitnkcom.wiki.views',
    url(r'^$', 'index', name="wiki_index"),
    url(r'^(\d+)/$', 'get_article', name="wiki_article"),
)
