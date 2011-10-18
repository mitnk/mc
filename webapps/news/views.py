import os
import re
from urllib2 import URLError

from django.conf import settings
from django.core.files import File
from django.http import HttpResponse, Http404
from django.utils.encoding import smart_str

from common.utils import get_soup_by_url
from webapps.news.models import News
from webapps.tools import send_mail

def send_to_kindle(request):
    send_to = ['whgking@free.kindle.com']
    subject = "Hacker News Update"
    files = os.listdir(settings.HACKER_NEWS_DIR)
    if not files:
        return HttpResponse("No new articles")
    files = [os.path.join(settings.HACKER_NEWS_DIR, x) for x in files]
    text = "There are %s article updated." % len(files)
    send_mail(send_to, subject, text, files=files)
    for f in files:
        os.remove(f)
    return HttpResponse(text)

def save_to_file(url, title="untitled"):
    file_name = re.sub(r'[^0-9a-zA-Z- ]+', '', title)
    file_name = "%s.txt" % file_name.lower().replace(' ', '_')
    if not file_name:
        return

    file_name = os.path.join(settings.HACKER_NEWS_DIR, file_name)
    if os.path.exists(file_name):
        return

    try:
        soup = get_soup_by_url(url, timeout=3)
    except:
        return

    for kls in ("entry-content", "post", "copy", "article_inner", 
                "articleBody", 
                "blogbody", "realpost", "asset-body", "main"):
        content = soup.find("div", {"class": kls})
        if content:
            real_content = ''.join(content.findAll(text=True))
            if '<code' in real_content and '</code>' in real_content:
                return

            write_to_file(file_name, real_content)
            return

def write_to_file(file_name, content):
    f = File(open(file_name, "w"))
    f.write(smart_str(content))
    f.close()

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

        if points >= 100:
            save_to_file(tag['href'], tag.string)

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
