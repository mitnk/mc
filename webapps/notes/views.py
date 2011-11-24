import datetime
import re
import rfc822

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from common.utils import get_soup_by_url
from twitcn.tools import getPrivateApi
from webapps.notes.models import Note, Word

ASCII_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def index(request):
    notes = Note.objects.all()
    return render_to_response("webapps/notes.html",
        {'notes': notes},
        context_instance=RequestContext(request))


@csrf_exempt
def check_notes(request):
    if request.method != "POST" or request.POST.get("action") != "notes":
        return HttpResponse(":)")

    info = fetch_latest_urls()
    count = 0
    for url, added in info:
        notes = Note.objects.filter(url=url)
        words = Word.objects.filter(url=url)
        if notes.count() > 0 or words.count() > 0:
            continue
        save_note(url, added)
        count +=  1
    return HttpResponse("%s\n" % count)


def fetch_latest_urls():
    token = settings.TWITCN_PRIVATE_TOKEN
    api = getPrivateApi(token)
    messages = api.GetUserTimeline(user='mitnk')
    info = []
    for msg in messages:
        if "#Kindle" not in msg.text or 'http' not in msg.text:
            continue
        url = re.search(r'(http[^ ]+)', msg.text).group(1)
        added = datetime.datetime(*rfc822.parsedate(msg.created_at)[:6])
        info.append((url, added))
    return info


def save_note(url, date=None):
    soup = get_soup_by_url(url)
    tag = soup.find("div", {'class': 'highlightText'})
    text = ''.join(tag.findAll(text=True)).strip()
    tag = soup.find("div", {'class': 'note'})
    remark = ''.join(tag.findAll(text=True)).replace('Note:', '').replace('@zzrt', '').strip()

    cover_tag = soup.find('div', {'class': 'cover'})
    tag = cover_tag.find("span", {'class': 'title'})
    if tag:
        book = ''.join(tag.findAll(text=True)).strip()
        if 'Personal Document' in book:
            book = ''
    else:
        book = ''

    tag = cover_tag.find("span", {'class': 'author'})
    if tag:
        author = ''.join(tag.findAll(text=True)).replace(' by ', '').strip()
    else:
        author = ''

    if ' ' not in text \
        and text[0] in ASCII_CHARS \
        and text[-1] in ASCII_CHARS \
        and len(text) <= 64:
        if Word.objects.filter(word=text).count() == 0:
            Word.objects.create(url=url, word=text)
    else:
        note = Note()
        note.url = url
        note.text = text
        note.added = date or datetime.datetime.now()
        if remark:
            note.remark = remark
        if book:
            note.book = book
        if author:
            note.author = author
        note.save()
