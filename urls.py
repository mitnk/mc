from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

from public.feeds import LatestEntriesFeed
from common.sitemap import sitemaps

admin.autodiscover()

urlpatterns = patterns('',
    (r'^' + settings.URL_BLOG[1:], include('mitnkcom.blog.urls')),
    (r'^' + settings.URL_WIKI[1:], include('mitnkcom.wiki.urls')),
    (r'^' + settings.URL_PUBLIC[1:], include('mitnkcom.public.urls')),
    (r'^douqian/', include('webapps.douqian.urls')),
    (r'^t/', include('twitcn.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^sitemap\.xml', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^links/$', include('links.urls')),
    (r'^feed/$', LatestEntriesFeed()),
    (r'^webapps/', include('mitnkcom.webapps.urls')),
    (r'^dc/', include('mitnkcom.dailycost.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^ua/', "webapps.views.user_agent"),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/Users/mitnk/projects/mitnkcom/media/'}),)
