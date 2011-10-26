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
    try:
        soup = BeautifulSoup(page)
    except UnicodeEncodeError:
        try:
            soup = BeautifulSoup(page, fromEncoding='utf8')
        except UnicodeEncodeError:
            soup = BeautifulSoup(page, fromEncoding='gb18030')
    return soup

def write_to_file(file_name, content):
    f = File(open(file_name, "w"))
    f.write(smart_str(content))
    f.close()

def get_page_main_content(url, timeout):
    soup = get_soup_by_url(url, timeout=timeout)
    for tag in soup.findAll('br'):
        tag.replaceWith("\n")

    for tag in soup.findAll('p'):
        tag.insert(0, "\n")

    for tag in soup.findAll('pre'):
        tag.replaceWith("\n[Pre Code Removed]\n")

    for tag in soup.findAll('img'):
        tag.replaceWith("\n[Image]\n")

    for kls in ("post-bottom-area",
                "wp-caption", # wordpress images
                "entryDescription", # wired.com
                ):
        for tag in soup.findAll("div", {"class": re.compile(kls)}):
            tag.extract()

    for style in soup.findAll("style"):
        style.extract()

    html_parser = HTMLParser.HTMLParser()
    content = ""
    for kls in ("entry-content", # wordpress
                "articleContent",
                "postBody", # http://news.cnet.com
                "post-body", # blogspot
                "article_inner",
                "articleBody",
                "storycontent",
                "blogbody",
                "realpost",
                "asset-body",
                "entry",
                "post",
                "copy",
                "main"):
        if len(kls) >= 8:
            tags = soup.findAll("div", {"class": re.compile(kls)})
        else:
            tags = soup.findAll("div", {"class": kls})
        if not tags:
            continue
        for tag in tags:
            text = ''.join(tag.findAll(text=True))
            text = re.sub(r'\r*\n+', '\n', text)
            content += html_parser.unescape(text)
        break
    return content.strip()
