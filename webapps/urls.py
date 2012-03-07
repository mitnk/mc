from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'webapps.views.index'),
    (r'^ckeditor/$', 'webapps.views.ckeditor'),
    (r'^send_tweets_to_kindle/$', 'webapps.views.send_tweets_to_kindle'),
    (r'^zongheng/', include('webapps.zongheng.urls')),
)
