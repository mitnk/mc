import re
import urllib2
from bs4 import BeautifulSoup


USER_AGENT = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16"
ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
COOKIE = 'WAPPageSize=0'
HEADERS = [('User-agent', USER_AGENT), ("Accept", ACCEPT), ("Cookie", COOKIE)]


def get_chapter_list(book_id, asc=0, page=1):
    """
    >>> L = get_chapter_list(48552, asc=1, page=3); print len(L), L[0], L[-1]
    20 1215151 1232898
    """
    if not book_id:
        return []

    try:
        url = 'http://m.zongheng.com/chapter/list?bookid=%s&asc=%s&pageNum=%s'
        opener = urllib2.build_opener()
        opener.addheaders = HEADERS
        page = opener.open(url % (book_id, asc, page))
    except (urllib2.HTTPError, urllib2.URLError):
        return []

    soup = BeautifulSoup(page, from_encoding="utf-8")
    tag = soup.find("div", {"class": "list"})
    if not tag:
        return []

    chapter_id_list = []
    for href in [x['href'] for x in tag.findAll('a')]:
        results = re.search(r'cid=(\d+)', href)
        if results:
            chapter_id_list.append(int(results.group(1)))
    return chapter_id_list

def get_book_name(book_id):
    """
    >>> get_book_name(45669)
    u'\u4fee\u771f\u4e16\u754c'
    """
    url = 'http://m.zongheng.com/book?bookid=%s' % book_id
    opener = urllib2.build_opener()
    opener.addheaders = HEADERS
    name = ""
    try:
        page = opener.open(url)
        soup = BeautifulSoup(page, from_encoding="utf-8")
    except (urllib2.HTTPError, urllib2.URLError):
        pass
    else:
        name = soup.find("h2").find("a").string.strip().strip(u'\u300a\u300b')
    return name

def get_chapter_content(book_id, chapter_id):
    """
    >>> abs(len(get_chapter_content(45669, 1843837)) - 3395) < 10
    True
    """
    url = 'http://m.zongheng.com/chapter?bookid=%s&cid=%s' % (book_id, chapter_id)
    opener = urllib2.build_opener()
    opener.addheaders = HEADERS
    page = opener.open(url)
    soup = BeautifulSoup(page, from_encoding="utf-8")
    tag = soup.find("div", {"class": "yd"})
    metas = tag.findAll(["a", "span"])
    for meta in metas:
        meta.extract()
    p_tags = tag.findAll("p")
    for p in p_tags:
        if p.string and isinstance(p.string, unicode):
            p.string = p.string + "\r\n"
        else:
            p.string = "\r\n"
    return tag.get_text()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
