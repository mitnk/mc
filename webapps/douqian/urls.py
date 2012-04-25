from django.conf.urls import patterns, url

urlpatterns = patterns('mitnkcom.webapps.douqian.views',
    url(r'^$', 'index', name="douqian_index"),
    url(r'^read/(\d+)/$', 'read_detail', name="read_detail"),
    url(r'^read/(\d+)/edit/$', 'read_edit', name="read_edit"),
    url(r'^logout/$', 'logout', name="douqian_logout"),
    url(r'^login_with_douban/$', 'login_with_douban', name="login_with_douban"),
    url(r'^douban_callback/$', 'douban_callback', name="douban_callback"),
)
