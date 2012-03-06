import datetime
import os.path
import urllib2
import time

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt

from webapps.zongheng.models import Novel
from webapps.tools import send_mail
from utils.zongheng import get_chapter_list, get_chapter_content, get_book_name


@csrf_exempt
def kindle(request):
    if request.method == "POST":
        book_id = request.POST.get('book_id', 0)
        if not book_id:
            return HttpResponse("Invalid book_id")

        book_name = get_book_name(book_id)
        if not book_name:
            return HttpResponse("Cannot get book_name, zongheng lib broken?")

        if Novel.objects.filter(book_id=book_id).exists():
            novel = Novel.objects.get(book_id=book_id)
            if novel.title != book_name:
                novel.title = book_name
                novel.save()
        else:
            novel = Novel.objects.create(title=book_name, book_id=book_id)
        
        chapter_list = get_chapter_list(book_id)
        chapter_list = [x for x in chapter_list if int(x[0]) > int(novel.last_id)]
        if len(chapter_list) < settings.MIN_CHAPTER_COUNT:
            return HttpResponse("Not enough chapters.(%s/%s)\n" % (len(chapter_list), settings.MIN_CHAPTER_COUNT))

        chapter_list.reverse()
        file_name = write_to_file(book_id, chapter_list, book_name=book_name)
        if not settings.DEBUG:
            send_to_kindle(file_name)
        novel.last_id = max([int(x) for x, y in chapter_list])
        novel.save()
        return HttpResponse("Send %s chapters to your kindle\n" % len(chapter_list))


    novels = Novel.objects.all()
    return render_to_response('zongheng/kindle.html',
                              {'novels': novels, })


def send_to_kindle(file_name):
    send_to = [settings.MY_KINDLE_MAIL,]
    subject = "Zong Heng Novels Update"
    files = [file_name]
    send_mail(send_to, subject, "Zongheng Updated.", files=files)


def write_to_file(book_id, chapter_list, book_name):
    if not chapter_list:
        return

    if len(chapter_list) == 1:
        file_name = "%s(%s).txt" % (book_name, chapter_list[0].split(' ')[0])
    else:
        left = chapter_list[0][1].split(' ')[0]
        right = chapter_list[-1][1].split(' ')[0]
        file_name = "%s(%s-%s).txt" % (book_name, left, right)
    file_name = os.path.join(settings.ZONGHENG_DIR, file_name)
    with open(file_name, "w") as f:
        for cid, titile in chapter_list:
            content = "\r\n" + get_chapter_content(book_id, cid)
            f.write(smart_str(content))
            time.sleep(0.3) # sleep a while to be gentle
    return file_name

