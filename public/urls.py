from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'public.views.index'),
    (r'^category/(\d+)/$', 'public.views.get_category'),
    
    # old url for a single article
    (r'^article/(\d+)/$', 'public.views.get_article'),

    # new url for a single article
    (r'^(\d+)/$', 'public.views.get_article'),
)
