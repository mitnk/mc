#coding=utf-8
'''
Created on 2009-6-12
@author: mitnk
'''
import datetime
import re
import time
from django import template
from mitnkcom.twitcn.tools import get_root_path


register = template.Library()

def ParseReplyProc(res):
    reply = res.group('reply')
    return '<a href="%s/%s/">%s</a>' % (get_root_path(), reply[1:], reply)

def ParseUrlProc(res):
    url = res.group('url')
    if 't.co' in url:
        new_url = url.split('/')[-1]
    else:
        new_url = url
    return '<a href="%s/tco/%s">%s</a>' % (get_root_path(), new_url, url)

@register.filter
def ParseStatusText(value):
    if not value:
        return value
    p1 = re.compile(r'(?P<reply>@[a-zA-Z0-9_]+)', re.VERBOSE)
    p2 = re.compile(r'(?P<url>http://t.co/\w+)', re.VERBOSE)
    value = p1.sub(ParseReplyProc, value)
    value = p2.sub(ParseUrlProc, value)
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
