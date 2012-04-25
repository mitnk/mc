from django.conf.urls import patterns, url


urlpatterns = patterns('mitnkcom.blog.views',
    url(r'^$', 'index', name="blog_index"),
    url(r'^article/(\d+)/$', 'get_article', name="blog_article"),
)
