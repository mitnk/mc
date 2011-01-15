#coding=utf-8
'''
Created on 2009-6-7

@author: mitnk
'''
from django.utils import simplejson
import re
import urllib
import urllib2
import datetime
from config import CONSUMER_KEY, CONSUMER_SECRET, TWITCN_ROOT_PATH
import twitter, oauth
from oauthtwitter import OAuthApi
from BeautifulSoup import BeautifulSoup
 
def getPrivateApi():
    access_token = oauth.Token.from_string("oauth_token_secret=9Bjtq4wSHL4Vm3mTGi8y1rWAFFvsdUgxnhPHTnNp8&oauth_token=23502724-2D6P9yR82kszjsRx7UavvbYAlWU06OpEW45h2tUbY")
    api = OAuthApi(CONSUMER_KEY, CONSUMER_SECRET, 
                   access_token.key, access_token.secret, verified=True)
    return api

def getOldUrl(bitly_url):
    try:
        page = urllib2.urlopen('http://bit.ly/' + bitly_url + '+')
        soup = BeautifulSoup(page)
        return soup.find("dl", "info-snapshot").ddTag.aTag["href"]
    except:
        pass
    return 'http://bit.ly/' + bitly_url

def getShortUrl(url):
    try:
        short_url = "http://is.gd/api.php?longurl=" + urllib.quote(url)
        content = urllib2.urlopen(short_url).read()
        return content
    except:
        pass
    return ""


def shortenUrlsProc(res):
    url = res.group('url')
    if len(url) > 30:
        short_url = getShortUrl(url)
        return short_url if short_url else url
    return url

def shortenStatusUrls(text):
    try:
        p = re.compile(r'(?P<url>https?://[^ ]+)', re.VERBOSE)
        return p.sub(shortenUrlsProc, text)
    except:
        return text

def getTwitterApi(request, update=False):
    api = None
    user = None
    access_token = request.session.get('access_token')
    user_info = request.session.get('user_info')

    # login with oauth
    if access_token: 
        access_token = oauth.Token.from_string(access_token)
        api = OAuthApi(CONSUMER_KEY, CONSUMER_SECRET, 
                       access_token.key, access_token.secret, verified=True)

        if update or not user_info:
            user = api.GetUserInfo()
            request.session["user_info"] = user.AsJsonString()
        else:
            json = simplejson.loads(user_info)
            user = twitter.User.NewFromJsonDict(json)

    return api, user

def get_root_path():
    if TWITCN_ROOT_PATH == "/":
        return ""
    else:
        return "/" + TWITCN_ROOT_PATH.strip("/")

def twitcn_path(request):
    """Return root path of twitcn app."""
    return {'ROOT_PATH': get_root_path()}

