from django.conf.urls.defaults import *

urlpatterns = patterns('dailycost.views',
    url(r'^$', 'index', name="dailycost_index"),
)
