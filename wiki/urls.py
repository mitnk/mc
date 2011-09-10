from django.conf.urls.defaults import *

urlpatterns = patterns('wiki.views',
    url(r'^$', 'index', name="wiki_index"),
    url(r'^category/$', 'get_all_categories', name="wiki_all_category"),
    url(r'^article/(\d+)/$', 'get_article', name="wiki_article"),
    url(r'^category/(\d+)/$', 'get_category', name="wiki_category"),
)
