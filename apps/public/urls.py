from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'apps.public.views.index'),
    (r'^category/(\d+)/$', 'apps.public.views.get_category'),
    
    # old url for a single article
    (r'^article/(\d+)/$', 'apps.public.views.get_article'),

    # new url for a single article
    (r'^(\d+)/$', 'apps.public.views.get_article'),
)
