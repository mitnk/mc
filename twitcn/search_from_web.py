#coding=utf-8
from bs4 import BeautifulSoup
from urllib2 import urlopen
import re

def searchTwitterWeb(url):
    page = urlopen(url)
    soup = BeautifulSoup(page)
    
    res = soup.findAll("li", {"class":re.compile(r'^result[^#]{1,3}')})
    
    results = ""
    for r in res:
        source = str(r.find('div', 'info').find('span', 'source').aTag).replace('"', '\\"')
        results += '{"created_at":"' + r.find('div', 'info').contents[0].strip() + '",'
        results += '"from_user":"' + r.find('div', 'msg').aTag.string + '",'
        results += '"source":"' + source + '",'
        results += '"profile_image_url":"' + r.find('div', {'class': 'avatar'}).find('img')['src'] + '",'
        
        span_tag_content = r.find('div', 'msg').spanTag
        spanGen = span_tag_content.recursiveChildGenerator()
        
        text = ''
        for e in spanGen:
            if isinstance(e,unicode):
                text += e
        text = text.replace('"', '\\"')
        text = text.replace("\\", "")
        text = text.replace("\b", "")
        text = text.replace("\t", "")
        text = text.replace("\f", "")
        text = text.replace("\n", "")
        text = text.replace("\r", "")
        text = text.replace("\t", "")

        results += '"text":"' + text + '",'
        
        foo = re.search(r'<span id="msgtxt(\d+)"', unicode(span_tag_content))
        if foo:
            results += '"id":' + foo.group(1) + ','
            
        results += '"from_user_id":11111},'
        
    results = results[:-1]
    
    assert results
    return '{"results":[' + results + ']}'

def searchBingTwitter(url):
    page = urlopen(url)
    soup = BeautifulSoup(page)
    res = soup.find("ul", "sn_ul sn_toul sn_tweets").findAll('li')
    
    results = ""
    for r in res:
        status_info = r.find('div', 'sn_status').find('span', 'sn_time').find('a', 'sn_nowrap')
        try:
            status_id = re.search(r'/status/(\d+)', status_info['href']).group(1)
        except:
            status_id = 0
        
        results += '{"created_at":"' + status_info.string + '",'
        results += '"from_user":"' + r.find('div', 'sn_status').find('a').string + '",'
        results += '"profile_image_url":"' + r.find('img')['src'] + '",'
        
        r.find('div', 'sn_status').find('span', 'sn_time').extract()
        r.find('div', 'sn_status').find('a').extract()
        text = u''.join([e for e in r.find('div', 'sn_status').recursiveChildGenerator() if isinstance(e,unicode)])

        text = text.replace(":&nbsp;", "")
        text = text.replace('"', '\\"')
        text = text.replace("\\", "")
        text = text.replace("\b", "")
        text = text.replace("\t", "")
        text = text.replace("\f", "")
        text = text.replace("\n", "")
        text = text.replace("\r", "")
        text = text.replace("\t", "")
        text = text.replace("&#32;", " ")

        results += '"text":"' + text + '",'
        
        results += '"id":' + status_id + '},'
        
    results = results[:-1]
    
    assert results
    return '{"results":[' + results + ']}'
