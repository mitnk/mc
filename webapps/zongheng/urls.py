from django.conf.urls import patterns, url

urlpatterns = patterns('mitnkcom.webapps.zongheng.views',
    url(r'^$', 'index', name="zongheng_index"),
    (r'^kindle/', 'kindle'),
)
