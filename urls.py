from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

from apps.public.feeds import LatestEntriesFeed
from apps.common.sitemap import sitemaps

admin.autodiscover()

urlpatterns = patterns('',
    (r'^' + settings.URL_BLOG[1:], include('mitnkcom.apps.blog.urls')),
    (r'^' + settings.URL_WIKI[1:], include('mitnkcom.apps.wiki.urls')),
    (r'^' + settings.URL_PUBLIC[1:], include('mitnkcom.apps.public.urls')),
    (r'^t/', include('apps.twitcn.urls')),
    (r'^$', 'mitnkcom.views.index'),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^sitemap\.xml', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^links/$', include('apps.links.urls')),
    (r'^feed/$', LatestEntriesFeed()),

    (r'^category/$', 'apps.public.views.get_all_categories'),
    (r'^about/$', 'apps.public.views.about'),

    (r'^webapps/', include('mitnkcom.webapps.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/home/mitnk/projects/mitnkcom/media/'}),)

