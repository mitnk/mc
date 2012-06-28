import en
import re
import string
import time
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

def is_basic_word(word):
    return word.lower() in en.basic.words

def is_ascii(s):
    for c in s:
        if c not in string.ascii_letters:
            return False
    return True

def basic_filter(words):
    return [x for x in words if not is_basic_word(x[0])]

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

    ## noun plural to singular
    try:
        if en.is_noun(word):
            new_word = en.noun.singular(word)
            if new_word != word and en.is_noun(new_word):
                return new_word
    except KeyError:
        pass

    ## noun, convert "er, or" to verb
    try:
        if en.is_noun(word):
            new_word = re.sub(r'er$', '', word)
            if new_word != word and en.is_verb(new_word):
                return new_word
    except KeyError:
        pass

    try:
        if en.is_noun(word):
            new_word = re.sub(r'r$', '', word)
            if new_word != word and en.is_verb(new_word):
                return new_word
    except KeyError:
        pass

    ## adv to adj
    ## TODO: is there a quick way to do this in "en" libs
    try:
        new_word = re.sub(r'ly$', '', word)
        if new_word != word and en.is_adjective(new_word):
            return new_word
    except KeyError:
        pass

    try:
        if word.endswith('ly'):
            new_word = re.sub(r'ly$', '', word) + 'e'
            if new_word != word and en.is_adjective(new_word):
                return new_word
    except KeyError:
        pass

    try:
        new_word = re.sub(r'y$', '', word)
        if new_word != word and en.is_adjective(new_word):
            return new_word
    except KeyError:
        pass

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
        result = "\n".join(['%s%4s' % (x[0].ljust(30), x[1]) for x in words])
        title = "=" * 40 + '\n'
        title += 'Run time: %.3f seconds\n' % (time.time() - t)
        result += '\n' + title
        return HttpResponse(result, mimetype="text/plain")
    return render(request, 'english/index.html', result)

