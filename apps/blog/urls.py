from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'apps.blog.views.index'),
    (r'^category/$', 'apps.blog.views.get_all_categories'),
    (r'^article/(\d+)/$', 'apps.blog.views.get_article'),
    (r'^category/(\d+)/$', 'apps.blog.views.get_category'),
)
