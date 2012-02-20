#coding=utf-8
'''
Created on 2009-6-7

@author: mitnk
'''
from bs4 import BeautifulSoup
from oauthtwitter import OAuthApi
import datetime
import re
import twitter, oauth
import urllib
import urllib2

from django.conf import settings
from django.utils import simplejson

def getPrivateApi(token):
    access_token = oauth.Token.from_string(token)
    api = OAuthApi(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, 
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
        api = OAuthApi(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, 
                       access_token.key, access_token.secret, verified=True)

        if update or not user_info:
            user = api.GetUserInfo()
            request.session["user_info"] = user.AsJsonString()
        else:
            json = simplejson.loads(user_info)
            user = twitter.User.NewFromJsonDict(json)

    return api, user

def get_root_path():
    if settings.TWITCN_ROOT_PATH == "/":
        return ""
    else:
        return "/" + settings.TWITCN_ROOT_PATH.strip("/")

def twitcn_path(request):
    """Return root path of twitcn app."""
    return {'ROOT_PATH': get_root_path()}

