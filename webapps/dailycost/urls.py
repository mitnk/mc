from django.conf.urls.defaults import *

urlpatterns = patterns('mitnkcom.webapps.dailycost.views',
    url(r'^$', 'index', name="dailycost_index"),
)
