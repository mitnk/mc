from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'webapps.notes.views.index', name='notes_index'),
)
