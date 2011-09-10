from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'links.views.index', name="links"),
)
