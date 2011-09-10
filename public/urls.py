from django.conf.urls.defaults import *

urlpatterns = patterns('public.views',
    url(r'^$', 'index', name="public_index"),
    url(r'^category/$', 'get_all_categories', name="public_all_category"),
    url(r'^commands/$', 'linux_commands', name="public_commands"),
    url(r'^category/(\d+)/$', 'get_category', name="public_category"),

    # old url for a single article
    url(r'^article/(\d+)/$', 'get_article', name="public_article_old"),
    # new url for a single article
    url(r'^(\d+)/$', 'get_article', name="public_article"),
)
