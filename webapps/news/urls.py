from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'webapps.news.views.index'),
)
