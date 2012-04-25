from django.conf.urls.defaults import *

urlpatterns = patterns('mitnkcom.webapps.views',
    (r'^$', 'index'),
    (r'^ckeditor/$', 'ckeditor'),
    (r'^send_tweets_to_kindle/$', 'send_tweets_to_kindle'),
    (r'^zongheng/', include('mitnkcom.webapps.zongheng.urls')),
)
