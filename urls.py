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
    (r'^dc/', include('mitnkcom.webapps.dailycost.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^meta/$', "webapps.views.http_meta"),
    (r'^hn/$', "webapps.news.views.index"),
    url(r'^twp/$', "twitcn.views.private_tweets", name="private_tweets"),
    (r'^twp/c/$', "twitcn.views.private_clear_session"),
    (r'^twp/d/$', "twitcn.views.private_dm"),
    (r'^twp/f/$', "twitcn.views.private_favorites"),
    (r'^twp/m/$', "twitcn.views.private_mention"),
    (r'^twp/re/$', "twitcn.views.private_retweets_of_me"),
    (r'^favo/$', "webapps.views.favo_tweets"),
    (r'^tweets/$', "webapps.views.my_tweets"),
    (r'^notes/$', include('webapps.notes.urls')),
    (r'^check_notes/$', 'webapps.notes.views.check_notes'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/Users/mitnk/projects/mitnkcom/media/'}),)
