from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'blog.views.index'),
    (r'^category/$', 'blog.views.get_all_categories'),
    (r'^article/(\d+)/$', 'blog.views.get_article'),
    (r'^category/(\d+)/$', 'blog.views.get_category'),
)
