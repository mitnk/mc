from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^check_website/$', 'webapps.views.check_website'),
    (r'^user_agent/$', 'webapps.views.user_agent'),
    (r'^send_tweets_to_kindle/$', 'webapps.views.send_tweets_to_kindle'),
    (r'^zongheng/', include('webapps.zongheng.urls')),
)
