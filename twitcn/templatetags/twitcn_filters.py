#coding=utf-8
'''
Created on 2009-6-12
@author: mitnk
'''
from django import template
from datetime import timedelta
import re
from twitcn.tools import get_root_path

register = template.Library()

def ParseReplyProc(res):
    reply = res.group('reply')
    return '<a href="%s/%s/">%s</a>' % (get_root_path(), reply[1:], reply)

def ParseUrlProc(res):
    url = res.group('url')
    if "http://bit.ly/" in url:
        foo = url.replace('http://bit.ly/', '')
        return '<a class="bitly-url" href="%s/bitly/%s" target="_blank">%s</a>' % (get_root_path(), foo, url)
    return '<a href="%s" target="_blank">%s</a>' % (url, url)

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
        value = value + timedelta(hours = int(arg))
    except:
        pass
    return value
