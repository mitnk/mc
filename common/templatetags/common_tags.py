import re

from django import template
from django.conf import settings

import pygments
from pygments.lexers import guess_lexer, get_lexer_by_name, PythonLexer
from pygments.formatters import HtmlFormatter

register = template.Library()

@register.filter
def pygmentize(value):
    value = value.replace('\n', '')
    regex = re.compile(r'<code(.*?)</code>', re.DOTALL)
    last_end = 0
    to_return = ''
    found = 0
    for match_obj in regex.finditer(value):
        code_string = match_obj.group(1)

        # determin lexer name by class name
        # then remove class attribute
        lexer = PythonLexer()
        if code_string.startswith(' class='):
            res = re.search(r'^ class="(.*?)">', code_string)
            code_string = code_string.replace(res.group(), '')
            if res:
                lexer_name = res.group(1)
                try:
                    lexer = get_lexer_by_name(lexer_name)
                except:
                    pass
        else:
            # remove the start charater '<'
            code_string = code_string[1:]

        pygmented_string = pygments.highlight(code_string, lexer, HtmlFormatter())
        to_return = to_return + value[last_end:match_obj.start(1)].replace('\r', '<br />') + pygmented_string
        last_end = match_obj.end(1)
        found = found + 1
    to_return = to_return + value[last_end:].replace('\r', '<br />')
    return to_return


@register.filter
def get_first_path(url):
    """
    >>> from django.conf import settings
    >>> get_first_path("/")
    '/'
    >>> get_first_path("/foo")
    '/'
    >>> get_first_path("/foo/")
    '/'
    >>> get_first_path("/foo/bar/")
    '/'
    >>> get_first_path(settings.URL_BLOG + "abc/") == settings.URL_BLOG
    True
    >>> get_first_path(settings.URL_WIKI + "abc/") == settings.URL_WIKI
    True
    >>> get_first_path(settings.URL_PUBLIC + "abc/") == settings.URL_PUBLIC
    True
    """
    if not url or url == '/':
        return '/'

    path = '/'
    index = url[1:].find('/')
    if index != -1:
        path = url[:index + 2]
        if path in (settings.URL_PUBLIC, settings.URL_WIKI, settings.URL_BLOG):
            return path
    return '/'
