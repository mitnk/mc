from django.conf.urls.defaults import *

urlpatterns = patterns('mitnkcom.webapps.zongheng.views',
    url(r'^$', 'index', name="zongheng_index"),
    (r'^kindle/', 'kindle'),
)
