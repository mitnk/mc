from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'links.views.index'),
)
