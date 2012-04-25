from django.conf.urls import patterns, url

urlpatterns = patterns('mitnkcom.links.views',
    url(r'^$', 'index', name="links"),
)
