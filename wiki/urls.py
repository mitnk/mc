from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'wiki.views.index'),
    (r'^category/$', 'wiki.views.get_all_categories'),
    (r'^article/(\d+)/$', 'wiki.views.get_article'),
    (r'^category/(\d+)/$', 'wiki.views.get_category'),
)
