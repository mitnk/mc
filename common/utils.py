import datetime
import urllib2

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
