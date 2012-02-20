import os
import re
from urllib2 import URLError
from tempfile import NamedTemporaryFile

from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from common.utils import get_soup_by_url, write_to_file
from webapps.news.models import News, Archive
from webapps.tools import send_mail

from external_libs.briticle import Briticle

import logging
logger = logging.getLogger("BRITICLE")
if not logger.handlers:
    handler = logging.FileHandler(settings.LOG_BRITICLE)
    formatter = logging.Formatter('%(asctime)s %(levelname)s\n%(message)s\n')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def send_to_kindle(request):
    send_to = settings.KINDLE_SENDING_LIST
    subject = "Hacker News Update"
    files = os.listdir(settings.HACKER_NEWS_DIR)
    if not files:
        return HttpResponse("No new articles")
    files = [os.path.join(settings.HACKER_NEWS_DIR, x) for x in files if x.endswith('.mobi')]
    text = "There are %s article updated." % len(files)
    send_mail(send_to, subject, text, files=files)
    for f in files:
        try:
            os.remove(f)
        except OSError:
            pass
    return HttpResponse(text)


def save_to_file(url, dir_name=settings.HACKER_NEWS_DIR, title=None, force=False):
    """ TODO: Add force update param """
    if not force and Archive.objects.filter(url=url).count() > 0:
        return

    try:
        br = Briticle(url)
        if not br.content:
            logger.info("No content found at url: %s" % url)
            return None

        page_title, content = br.title, br.content
        if not title:
            title = page_title
        file_name = re.sub(r'[^0-9a-zA-Z _-]+', '', title).replace(' ', '_') or 'blank_name'
        mobi_name = "%s.mobi" % file_name
        html_name = "%s.html" % file_name
        file_path = br._save_to_html(html_name, dir_name)

        if not Archive.objects.filter(url=url):
            archive = Archive(url=url, file_name=title)
            archive.save()

        if not file_path or not os.path.exists(file_path):
            logger.info('File not found for URL: %s' % url)
            return None

        cmd = "kindlegen %s -o %s > /dev/null" % (file_path, mobi_name)
        os.system(cmd)
        mobi_file = re.sub(r'\.html$', '.mobi', file_path)
        if not os.path.exists(mobi_file):
            logger.info("Failed to generate mobi file. URL: %s" % url)

        # Remove all middle-files except .MOBI
        file_list = os.listdir(dir_name)
        for f in file_list:
            if not f.endswith(".mobi"):
                try:
                    os.remove(dir_name + "/" + f)
                except OSError:
                    pass
        return mobi_file

    except Exception, e:
        if isinstance(e, URLError) or 'timed out' in str(e):
            logger.info("URLError / Time out Exception: %s URL: %s" % (e, url)
            return None
        else:
            logger.info("Exception: %s URL: %s" % (e, url)


@csrf_exempt
def index(request):
    if request.method != "POST":
        return render_to_response('webapps/hacker_news.html')

    url = request.POST.get('url', '')
    if not url:
        return HttpResponse("URL needed.")

    if request.POST.get('url') != "HN":
        mobi_file = save_to_file(url, dir_name=settings.KINDLE_LIVE_DIR, force=True)
        if mobi_file:
            send_mail([settings.MY_KINDLE_MAIL,], "New documentation here", "Sent from mitnk.com", files=[mobi_file,])
            os.remove(mobi_file)
            return HttpResponse("%s Sent!" % mobi_file)
        else:
            return HttpResponse("No file sent!")
    elif request.POST.get('url') == "HN":
        url = 'http://news.ycombinator.com/'
        try:
            soup = get_soup_by_url(url)
        except:
            return HttpResponse("Time Out")

        tags = soup.find("table").findAll("td", {"class": "title"})
        count = 0
        for t in tags:
            tag = t.find('a')
            if not tag:
                continue
            elif tag.string.lower() == "more" and '/' not in tag['href']:
                continue

            try:
                points = int(t.parent.nextSibling.find('span').string.split(' ')[0])
            except AttributeError, ValueError:
                points = 0
            if points < settings.POINTS_LIMIT_TO_LOG:
                continue

            if 'http' not in tag['href']:
                tag['href'] = "http://news.ycombinator.com/" + tag['href']

            if points >= settings.POINTS_LIMIT_TO_KINDLE:
                save_to_file(tag['href'], title=tag.string)

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
