from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'webapps.views.index'),
    (r'^ckeditor/$', 'webapps.views.ckeditor'),
    (r'^check_website/$', 'webapps.views.check_website'),
    (r'^send_tweets_to_kindle/$', 'webapps.views.send_tweets_to_kindle'),
    (r'^zongheng/', include('webapps.zongheng.urls')),
    (r'^news/', include('webapps.news.urls')),
)
