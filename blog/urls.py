from django.conf.urls.defaults import *

urlpatterns = patterns('blog.views',
    url(r'^$', 'index', name="blog_index"),
    url(r'^article/(\d+)/$', 'get_article', name="blog_article"),
)
