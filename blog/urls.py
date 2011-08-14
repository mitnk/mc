from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^category/$', 'blog.views.get_all_categories'),
    (r'^article/(\d+)/$', 'blog.views.get_article'),
    (r'^category/(\d+)/$', 'blog.views.get_category'),
)
