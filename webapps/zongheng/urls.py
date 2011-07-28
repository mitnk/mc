from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^kindle/', 'webapps.zongheng.views.kindle'),
)
