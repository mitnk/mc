from django.contrib.syndication.views import Feed
from public.models import Article

class LatestEntriesFeed(Feed):
    title = "mitnk's blog"
    link = "http://mitnk.com"
    description = "Updates on mitnk.com"
    description_template = "description.html"

    def items(self):
        return Article.objects.order_by('-added')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_pubdate(self, item):
        return item.added

