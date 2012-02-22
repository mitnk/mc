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
        for tag in tags:
            tag_a = tag.find('a')
            if (not tag_a) or \
                ('href' not in tag_a.attrs) or \
                (len(tag_a.contents) > 1) or \
                (tag_a.string.lower() == "more" and '/' not in tag_a['href']):
                continue

            try:
                points = int(tag.parent.nextSibling.find('span').string.split(' ')[0])
            except AttributeError, ValueError:
                logger.error("No points found. URL: %s" % tag_a['href'])
                points = 0

            if 'http' not in tag_a['href']:
                tag_a['href'] = "http://news.ycombinator.com/" + tag_a['href']

            if tag_a['href'] and points >= self.POINTS_MIN_LIMIT and (not is_home_page(tag_a['href'])):
                self.articles.append({
                    'url': tag_a['href'],
                    'title': tag_a.string,
                    'points': points,
                })
