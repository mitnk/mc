from django.contrib.sitemaps import Sitemap
from mitnkcom.public.models import Article as PublicArticle
from mitnkcom.wiki.models import Article as WikiArticle
import datetime


class PublicSitemap(Sitemap):
    changefreq = 'weekly'

    def items(self):
        return PublicArticle.objects.all()

    def lastmod(self, obj):
        return obj.added

class WikiSitemap(Sitemap):
    changefreq = 'weekly'

    def items(self):
        return WikiArticle.objects.all()

    def lastmod(self, obj):
        return obj.added

sitemaps = {'blog': PublicSitemap, 'wiki': WikiSitemap}
