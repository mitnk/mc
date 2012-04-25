# coding=utf-8
import re
import time

from django.conf import settings

from mitnkcom.common.utils import get_soup_by_url
from mitnkcom.webapps.douqian import pydouban
from mitnkcom.webapps.douqian.models import Book, Read, User

def get_api(request):
    if "oauth_token" not in request.session or \
        "oauth_token_secret" not in request.session:
        return None

    api = pydouban.Api()
    api.set_oauth(key=settings.DOUBAN_API_KEY, 
                  secret=settings.DOUBAN_SECRET,
                  acs_token=request.session["oauth_token"], 
                  acs_token_secret=request.session["oauth_token_secret"])
    return api


def get_reading(request):
    api = get_api(request)
    if not api:
        return []

    entries = api.get_collections(cat='book', status="reading")
    entries = entries['entry']
    reading_id_list = []
    books = []
    for entry in entries:
        book = {'id': entry['subject']['id']['t'].replace("http://api.douban.com/book/subject/", ""),
                'title': entry['subject']['title']['t']}
        reading_id_list.append(int(book['id']))
        for link in entry['subject']['link']:
            if link['rel'] == 'image':
                book['image'] = link['href']
        book['author'] = ", ".join([x['name']['t'] for x in entry['subject']['author']])
        books.append(book)

    update_book_and_read(request.session['douban_user_id'], books)
    user = User.objects.get(douban_id=request.session['douban_user_id'])
    reads = Read.objects.filter(user=user)
    return [r for r in reads if int(r.book.subject_id) in reading_id_list]


def get_book_pages(book_id):
    url = "http://book.douban.com/subject/%s/" % book_id
    soup = get_soup_by_url(url)
    tag = soup.find("div", {"id": "info"})
    result = re.search(r">页数:</span> (\d+)<br", str(tag))
    if result:
        return result.group(1)
    return 0


def update_book_and_read(douban_user_id, books):
    for b in books:
        book, created = Book.objects.get_or_create(subject_id=b['id'])
        if created:
            book.title = b['title']
            book.image = b['image']
            book.author = b['author']
            book.save()

        # Create a read for this
        user = User.objects.get(douban_id=douban_user_id)
        read, flag = Read.objects.get_or_create(user=user, book=book)
        if read.total == 0:
            # fetch pages form douban web
            pages = get_book_pages(book.subject_id)
            if pages:
                read.total = pages
                read.save()
            time.sleep(0.2) # fetching be gentle

