from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'apps.links.views.index'),
)
