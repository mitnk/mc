from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^check_website/$', 'webapps.views.check_website'),
    (r'^zongheng/', include('webapps.zongheng.urls')),
)
