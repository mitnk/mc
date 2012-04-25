from django.conf.urls import patterns, url

urlpatterns = patterns('mitnkcom.webapps.dailycost.views',
    url(r'^$', 'index', name="dailycost_index"),
)
