from django.contrib.syndication.views import Feed
from apps.public.models import Article

class LatestEntriesFeed(Feed):
    title = "mitnk's blog"
    link = "http://mitnk.com"
    description = "Updates on changes and additions to chicagocrime.org."
    description_template = "description.html"

    def items(self):
        return Article.objects.order_by('-added')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

