from django.conf.urls.defaults import *

urlpatterns = patterns('douqian.views',
    url(r'^$', 'index', name="douqian_index"),
)
