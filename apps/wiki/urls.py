from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'apps.wiki.views.index'),
    (r'^category/$', 'apps.wiki.views.get_all_categories'),
    (r'^article/(\d+)/$', 'apps.wiki.views.get_article'),
    (r'^category/(\d+)/$', 'apps.wiki.views.get_category'),
)
