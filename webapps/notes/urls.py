from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'webapps.notes.views.index', 'notes_index'),
)
