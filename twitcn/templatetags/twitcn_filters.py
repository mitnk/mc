#coding=utf-8
'''
Created on 2009-6-12
@author: mitnk
'''
import datetime
import re
import time

from django import template

import requests
from twitcn.tools import get_root_path


register = template.Library()

def is_shorten_url(url):
    SHORTEN_URLS = ("bit.ly", "t.co")
    for s in SHORTEN_URLS:
        if s + '/' in url:
            return True
    return False

def ParseReplyProc(res):
    reply = res.group('reply')
    return '<a href="%s/%s/">%s</a>' % (get_root_path(), reply[1:], reply)

def ParseUrlProc(res):
    url = res.group('url')
    if is_shorten_url(url):
        try:
            t = time.time()
            r_url = requests.get(url).url
            return '<a href="%s" class="%s">%s</a>' % (r_url, time.time() - t, url)
        except:
            pass
    return '<a href="%s">%s</a>' % (url, url)

def ParseSearchProc(res):
    search_tag = res.group('search')
    return '<a href="#" onclick=\'javascript:loadMoreStatus({"q": "%s", "page_name": "Real-time result for %s", "asker": "search", "first_time": true});\'>%s</a>' % (search_tag, search_tag, search_tag)

@register.filter
def ParseStatusText(value):
    if not value:
        return value
    
    p1 = re.compile(r'(?P<reply>@[a-zA-Z0-9_]+)', re.VERBOSE)
    p2 = re.compile(r'(?P<url>https?://[^ ]+)', re.VERBOSE)
    p3 = re.compile(r'(?P<search>\#[a-zA-Z0-9_]+)', re.VERBOSE)
    value = p1.sub(ParseReplyProc, value)
    value = p2.sub(ParseUrlProc, value)
    value = p3.sub(ParseSearchProc, value)
    return value

@register.filter
def GetShortDate(value):
    return value[4:10] + value[-5:]

@register.filter
def addHours(value, arg=0):
    try:
        value = value + datetime.timedelta(hours = int(arg))
    except:
        pass
    return value
