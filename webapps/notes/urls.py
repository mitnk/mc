from django.conf.urls import patterns, url

urlpatterns = patterns('mitnkcom.webapps.notes.views',
    url(r'^$', 'index', name='notes_index'),
)
