from bs4 import BeautifulSoup
import en
import re
import random
import json
import string
import time
import urllib

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from mitnkcom.english.basic import basic_words
from mitnkcom.english.models import Dict

def HttpResponseJson(result):
    status_code = 200
    if not isinstance(result, dict):
        status_code = 400
        result = {'status': 'failed', 'reason': result}
    return HttpResponse(json.dumps(result, indent=4),
                        status=status_code,
                        mimetype='application/json',
                        content_type = 'application/json; charset=utf8')


def api_lookup(request, w):
    result = {'key': w}
    word = normalize(w)
    try:
        record = Dict.objects.get(word=word)
        define = {'word': word}
        define['pos'] = record.pos
        define['pron'] = record.pron
        define['gloss'] = record.gloss
        define['acceptation'] = record.acceptation
        define['define'] = json.loads(record.define)
        result['result'] = define
        result['status'] = 'ok'
    except Dict.DoesNotExist:
        get_acceptation_from_web(word)
        result['status'] = 'not found'
    if request.GET.has_key('api'):
        return HttpResponseJson(result)
    else:
        ua = request.META.get("HTTP_USER_AGENT", '').lower()
        result['veer'] = (re.search(r'webos|iphone', ua) is not None)
        return render(request, 'english/word.html', result)

def get_acceptation_from_web(word):
    url = 'http://dict-co.iciba.com/api/dictionary.php?w=%s' % word
    page = urllib.urlopen(url)
    content = page.read()
    soup = BeautifulSoup(content)
    if not soup.dict.find_all('pron') or not soup.dict.find_all('pron'):
        return ''
    acceptation = soup.dict.acceptation.text.strip()
    pron = soup.dict.ps.text.strip()
    pos = soup.dict.pos.text.strip()
    poses = soup.dict.find_all('pos')
    acceptations = soup.dict.find_all('acceptation')
    define = {}
    i = 0
    for p in poses:
        define[p.text.strip()] = acceptations[i].text.strip()
        i += 1

    if not Dict.objects.filter(word=word).exists():
        define = json.dumps(define, indent=4)
        Dict.objects.create(word=word, pos=pos, acceptation=acceptation, pron=pron, define=define, gloss=get_gloss(word))
    t = random.random()
    time.sleep(t * 0.2)
    return acceptation

def get_define(word):
    try:
        w = Dict.objects.get(word=word)
        return u'[%s] %s %s' % (w.pron, w.pos, w.acceptation)
    except Dict.DoesNotExist:
        return ''

def is_ascii(s):
    for c in s:
        if c not in string.ascii_letters:
            return False
    return True

def basic_filter(words):
    return [x for x in words if not basic_words.has_key(x[0])]

def count_filter(words, count_limit):
    return [x for x in words if x[1] >= int(count_limit)]

def normalize_words(words):
    new_words = words.copy()
    for w in words:
        word = normalize(w)
        if word == w:
            continue
        c = words[w]
        if word in new_words:
            new_words[word] += c
        else:
            new_words[word] = c
        new_words.pop(w)
    return new_words

def normalize(word):
    ## TODO: make this function nicer (UT, shorter).

    ## all verb to present
    try:
        new_word = en.verb.present(word)
        if new_word != word and en.is_verb(new_word):
            return new_word
    except KeyError:
        pass

    new_word = en.noun.singular(word)
    if new_word != word and en.is_noun(new_word):
        return new_word

    if en.is_noun(word):
        new_word = re.sub(r'er$', '', word)
        if new_word != word and en.is_verb(new_word):
            return new_word
        new_word = re.sub(r'r$', '', word)
        if new_word != word and en.is_verb(new_word):
            return new_word
        new_word = re.sub(r'ment$', '', word)
        if new_word != word and en.is_verb(new_word):
            return new_word
        new_word = re.sub(r'ness', '', word)
        if new_word != word and en.is_adjective(new_word):
            return new_word

    ## adv to adj
    ## TODO: is there a quick way to do this in "en" libs
    new_word = re.sub(r'ly$', '', word)
    if new_word != word and en.is_adjective(new_word):
        return new_word

    if word.endswith('ly'):
        new_word = re.sub(r'ly$', '', word) + 'e'
        if new_word != word and en.is_adjective(new_word):
            return new_word

    if en.is_adjective(word):
        new_word = re.sub(r'ory$', '', word) + 'e'
        if new_word != word and en.is_verb(new_word):
            return new_word
        new_word = re.sub(r'ive$', '', word) + 'e'
        if new_word != word and en.is_verb(new_word):
            return new_word
        new_word = re.sub(r'ive$', '', word)
        if new_word != word and en.is_verb(new_word):
            return new_word
        new_word = re.sub(r'er$', '', word)
        if new_word != word and en.is_adjective(new_word):
            return new_word
        new_word = re.sub(r'r$', '', word)
        if new_word != word and en.is_adjective(new_word):
            return new_word

    return word


def rank_words(f):
    words = {}
    for line in f:
        for word in line.strip().lower().split(' '):
            if len(word) <= 2 or not word.strip() or  not is_ascii(word):
                continue
            if word in words:
                words[word] += 1
            else:
                words[word] = 1
    words = normalize_words(words)
    words = [(x, words[x]) for x in words]
    return sorted(words, key=lambda x: -x[1])

def get_gloss(word):
    if en.is_verb(word):
        return en.verb.gloss(word)
    elif en.is_adjective(word):
        return en.adjective.gloss(word)
    elif en.is_adverb(word):
        return en.adverb.gloss(word)
    elif en.is_noun(word):
        return en.noun.gloss(word)
    else:
        return en.wordnet.gloss(word)

def index(request):
    result = {}
    if request.method == 'POST':
        t = time.time()
        try:
            f = request.FILES.getlist('file')[0]
        except IndexError:
            return HttpResponseRedirect("/en/")
        words = rank_words(f)
        words = basic_filter(words)
        words = count_filter(words, request.POST.get('count_limit', 2))
        result = "\n".join(['%s%4s    %s' % (x[0].ljust(20), x[1], get_define(x[0])) for x in words])
        title = "=" * 40 + '\n'
        title += 'Run time: %.3f seconds\n' % (time.time() - t)
        result += '\n' + title
        return HttpResponse(result, mimetype="text/plain")
    return render(request, 'english/index.html', result)

