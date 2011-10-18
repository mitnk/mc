import re

from django.http import HttpResponse, Http404

from common.utils import get_soup_by_url
from webapps.news.models import News

def send_url_to_kindle(url, title=""):
    soup = get_soup_by_url(url)
    content = soup.find("div", {"class": "entry-content"})
    if content:
        return

def index(request):
    url = 'http://news.ycombinator.com/'
    soup = get_soup_by_url(url)
    tags = soup.find("table").findAll("td", {"class": "title"})
    count = 0
    for t in tags:
        tag = t.find('a')
        if not tag:
            continue
        elif tag.string.lower() == "more" and '/' not in tag['href']:
            continue

        points = int(t.parent.nextSibling.find('span').string.split(' ')[0])
        if points < 37:
            continue

        if 'http' not in tag['href']:
            tag['href'] = "http://news.ycombinator.com/" + tag['href']

        try:
            news = News.objects.get(url=tag['href'])
            news.title = tag.string
            news.points = points
            news.save()
        except News.DoesNotExist:
            news = News(url=tag['href'], points=points, title=tag.string)
            news.save()
        count += 1

    return HttpResponse("Find %s news" % count)
