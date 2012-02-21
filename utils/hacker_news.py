import settings
import logging

from common.utils import get_soup_by_url

logger = logging.getLogger("HackerNews")
if not logger.handlers:
    handler = logging.FileHandler(settings.LOG_BRITICLE)
    formatter = logging.Formatter('%(asctime)s %(levelname)s\n%(message)s\n')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

class HackerNews(object):
    POINTS_MIN_LIMIT = 70


    def __str__(self):
        return u"<HackerNews %s articles insider>" % len(self.articles)

    __unicode__ = __str__
    __repr__ = __str__

    def __init__(self, fetch=False):
        self.url = 'http://news.ycombinator.com/'
        self.articles = []
        if fetch:
            self.fetch()

    def fetch(self):
        def is_home_page(url):
            return '/' not in url.replace('//', '').strip('/')

        try:
            soup = get_soup_by_url(self.url)
        except:
            logger.info("Time out when fetching HackerNews.")
            return

        # Reset articles before fetching
        self.articles = []

        tags = soup.find("table").find_all("td", {"class": "title"})
        for t in tags:
            tag = t.find('a')
            if not tag:
                continue
            elif tag.string.lower() == "more" and '/' not in tag['href']:
                continue

            try:
                points = int(t.parent.nextSibling.find('span').string.split(' ')[0])
            except AttributeError, ValueError:
                points = 0

            if 'http' not in tag['href']:
                tag['href'] = "http://news.ycombinator.com/" + tag['href']

            if tag['href'] and points >= self.POINTS_MIN_LIMIT and (not is_home_page(tag['href'])):
                self.articles.append({
                    'url': tag['href'],
                    'title': tag.string,
                    'points': points,
                })
