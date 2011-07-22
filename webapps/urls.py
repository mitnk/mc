from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^zongheng/', include('webapps.zongheng.urls')),
)
