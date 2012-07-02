from django.conf.urls import patterns, url

urlpatterns = patterns('mitnkcom.english.views',
    url(r'^$', 'index', name="english_index"),
    url(r'^api/(\w+)/$', 'api_lookup', name="english_api_lookup"),
)
