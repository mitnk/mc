from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'webapps.news.views.index'),
    (r'^send_to_kindle/$', 'webapps.news.views.send_to_kindle'),
)
