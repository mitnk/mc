import datetime
import re
import urllib2
import HTMLParser

from django.core.files import File
from django.utils.encoding import smart_str

from bs4 import BeautifulSoup

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
            soup = BeautifulSoup(page, from_encoding='utf8')
        except UnicodeEncodeError:
            soup = BeautifulSoup(page, from_encoding='gb18030')
    return soup

def write_to_file(file_name, content):
    f = File(open(file_name, "w"))
    f.write(smart_str(content))
    f.close()

