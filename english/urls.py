from django.conf.urls import patterns, url

urlpatterns = patterns('mitnkcom.english.views',
    url(r'^$', 'index', name="english_index"),
    url(r'^upload/$', 'upload', name="english_upload"),
)