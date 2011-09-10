from django.conf.urls.defaults import *

urlpatterns = patterns('blog.views',
    url(r'^$', 'index', name="blog_index"),
    url(r'^category/$', 'get_all_categories', name="blog_all_category"),
    url(r'^article/(\d+)/$', 'get_article', name="blog_article"),
    url(r'^category/(\d+)/$', 'get_category', name="blog_category"),
)
