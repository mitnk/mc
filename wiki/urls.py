from django.conf.urls.defaults import *

urlpatterns = patterns('wiki.views',
    url(r'^$', 'index', name="wiki_index"),
    url(r'^category/$', 'get_all_categories', name="wiki_all_category"),
    url(r'^category/(\d+)/$', 'get_category', name="wiki_category"),

    # old url for a single article
    url(r'^article/(\d+)/$', 'get_article', name="wiki_article_old"),
    # new url for a single article
    url(r'^(\d+)/$', 'get_article', name="wiki_article"),
)
