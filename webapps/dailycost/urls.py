from django.conf.urls.defaults import *

urlpatterns = patterns('webapps.dailycost.views',
    url(r'^$', 'index', name="dailycost_index"),
)
