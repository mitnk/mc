from django.conf.urls import patterns, url

urlpatterns = patterns('mitnkcom.english.views',
    url(r'^$', 'index', name="english_index"),
    url(r'^google_us/$', 'google_us', name="english_google_us"),
    url(r'^api/(\w+)/$', 'api_lookup', name="english_api_lookup"),
)
