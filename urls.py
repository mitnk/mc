from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.conf import settings

from mitnkcom.public.feeds import LatestEntriesFeed
from mitnkcom.common.sitemap import sitemaps

admin.autodiscover()

urlpatterns = patterns('',
    (r'^' + settings.URL_BLOG[1:], include('mitnkcom.blog.urls')),
    (r'^' + settings.URL_WIKI[1:], include('mitnkcom.wiki.urls')),
    (r'^' + settings.URL_PUBLIC[1:], include('mitnkcom.public.urls')),
    (r'^douqian/', include('mitnkcom.webapps.douqian.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^sitemap\.xml', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^feed/$', LatestEntriesFeed()),
    (r'^webapps/', include('mitnkcom.webapps.urls')),
    (r'^dc/', include('mitnkcom.webapps.dailycost.urls')),
    (r'^en/', include('mitnkcom.english.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^meta/$', "mitnkcom.webapps.views.http_meta"),
    (r'^dict/(\w+)/$', "mitnkcom.english.views.api_lookup"),
    (r'^favo/$', "mitnkcom.webapps.views.favo_tweets"),
    (r'^notes/$', include('mitnkcom.webapps.notes.urls')),
    (r'^check_notes/$', 'mitnkcom.webapps.notes.views.check_notes'),
    (r'^%s/' % settings.TWITCN_ROOT_PATH.strip('/'), include('mitnkcom.twitcn.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/Users/mitnk/projects/mitnkcom/mitnkcom/media/'}),)
