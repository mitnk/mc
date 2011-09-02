import datetime
import os.path
import re
import urllib2
import time

from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.utils.encoding import smart_str
from django.template.defaultfilters import striptags
from django.views.decorators.csrf import csrf_exempt

from webapps.BeautifulSoup import BeautifulSoup

from webapps.zongheng.models import Novel
from webapps.tools import send_mail


def get_latest_id(book_id, last_id, page):
    if not book_id:
        return 0

    url = 'http://wap.zongheng.com/chapter/list?bookid=%s&asc=0&pageNum=%s'
    page = urllib2.urlopen(url % (book_id, page))
    soup = BeautifulSoup(page)
    tag = soup.find("div", {"class": "list"})

    if not tag:
        return 0

    cids = []
    for href in [x['href'] for x in tag.findAll('a')]:
        results = re.search(r'cid=(\d+)', href)
        if results and int(results.group(1)) > int(last_id):
            cids.append(int(results.group(1)))

    cids.reverse() # Make cid from DESC to ASC
    return cids


def ParseUstringProc(res):
    return ''


def write_content(book_id, cids, page):
    file_name = "zongheng_%s.txt" % datetime.datetime.now().strftime("%h-%d-%H-%M-%S")
    file_name = os.path.join(settings.ZONGHENG_DIR, file_name)
    f = open(file_name, "w")
    pattern = re.compile(r"\[|\]|u'[^']+'", re.VERBOSE)
    for cid in cids:
        url = 'http://wap.zongheng.com/chapter?bookid=%s&cid=%s&pageNum=%s' % (book_id, cid, page)
        opener = urllib2.build_opener()
        opener.addheaders.append(('Cookie', 'WAPPageSize=0'))
        page = opener.open(url)
        soup = BeautifulSoup(page)
        tag = soup.findAll("div", {"class": "yd"})[0]
        content = smart_str(tag.contents).replace(", <p>", "").replace("</p>", "\r\n\r\n")
        content = pattern.sub(ParseUstringProc, content)
        content = smart_str(striptags(content)) + "\r\n"
        f.write(content)
        time.sleep(0.3) # sleep a while to be gentle
    f.close()
    return file_name


def send_to_kindle(file_name, cids):
    send_to = ['whgking@free.kindle.com']
    subject = "Zong Heng Novels Update"
    text = "There are %s chapter updated." % len(cids)
    files = [file_name]
    send_mail(send_to, subject, text, files=files)


@csrf_exempt
def kindle(request):
    latest_id = 0
    res = 0
    if request.method == "POST":
        book_id = request.POST.get('book_id')
        page = request.POST.get('page') or 1

        try:
            novel = Novel.objects.get(book_id=book_id)
            last_id = novel.last_id
        except Novel.DoesNotExist:
            novel = None
            last_id = 0
        
        if request.POST.get('last_id'):
            last_id = request.POST['last_id']
            print "god", last_id

        cids = get_latest_id(request.POST.get('book_id', 0), last_id, page)
        if not cids:
            return HttpResponse("No new contents.(%s-%s)" % (book_id, last_id))

        file_name = write_content(book_id, cids, page=page)
        send_to_kindle(file_name, cids)

        if last_id != 0:
            novel.last_id = cids[-1]
            novel.save()
        return HttpResponse("Send %s chapters to your kindle" % len(cids))


    novels = Novel.objects.all()
    return render_to_response('zongheng/kindle.html',
                              {'novels': novels, })

