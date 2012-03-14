from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'webapps.zongheng.views.index', name="zongheng_index"),
    (r'^kindle/', 'webapps.zongheng.views.kindle'),
)
