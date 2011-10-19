import datetime
import re
import urllib2
import HTMLParser

from django.core.files import File
from django.utils.encoding import smart_str

from webapps.BeautifulSoup import BeautifulSoup


def get_1st_of_last_month(date_from=None):
    if not date_from:
        date_from = datetime.date.today()
    this_month = date_from.month
    year = date_from.year
    if this_month == 1:
        last_month = 12
        year = year - 1
    else:
        last_month = this_month - 1

    return datetime.date(year, last_month, 1)

def get_soup_by_url(url, timeout=10):
    page = urllib2.urlopen(url, timeout=timeout)
    return BeautifulSoup(page)

def write_to_file(file_name, content):
    f = File(open(file_name, "w"))
    f.write(smart_str(content))
    f.close()

def get_page_main_content(url, timeout):
    soup = get_soup_by_url(url, timeout=timeout)
    html_parser = HTMLParser.HTMLParser()
    content = ""
    for kls in ("entry-content", "post", "copy", "article_inner", 
                "articleBody", "storycontent",
                "blogbody", "realpost", "asset-body", "main"):
        tags = soup.findAll("div", {"class": kls})
        for tag in tags:
            text = ''.join(tag.findAll(text=True))
            if '<code' in text and '</code>' in text:
                continue
            text = re.sub(r'\n+', '\r\n\r\n', text)
            content += html_parser.unescape(text)

    if not content:
        print "No Content."

    return content
