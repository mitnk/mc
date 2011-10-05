from django.conf import settings

from douqian import pydouban
from douqian.models import Book, Read, User

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

    entries = api.get_collections(cat='book', status="reading")['entry']
    readings = []
    for entiry in entries:
        book = {'id': entiry['subject']['id']['t'].replace("http://api.douban.com/book/subject/", ""),
                'title': entiry['subject']['title']['t']}
        for link in entiry['subject']['link']:
            if link['rel'] == 'image':
                book['image'] = link['href']
        book['author'] = ", ".join([x['name']['t'] for x in entiry['subject']['author']])
        readings.append(book)

    update_book_and_read(request.session['douban_user_id'], readings)
    user = User.objects.get(douban_id=request.session['douban_user_id'])
    return Read.objects.filter(user=user)


def update_book_and_read(douban_user_id, readings):
    for r in readings:
        book, created = Book.objects.get_or_create(subject_id=r['id'])
        if created:
            book.title = r['title']
            book.image = r['image']
            book.author = r['author']
            book.save()

        # Create a read for this
        user = User.objects.get(douban_id=douban_user_id)
        Read.objects.get_or_create(user=user, book=book)

