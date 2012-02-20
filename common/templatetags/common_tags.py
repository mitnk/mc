import re
import markdown
from pygments import highlight
from pygments.lexers import guess_lexer, get_lexer_by_name, BashLexer
from pygments.formatters import HtmlFormatter

from django import template
from django.conf import settings
from bs4 import BeautifulSoup

register = template.Library()

@register.filter
def pygments_markdown(content):
    """Render this content for display.
    """
    # First, pull out all the <code></code> blocks, to keep them away
    # from Markdown (and preserve whitespace).
    soup = BeautifulSoup(content, "html.parser")
    code_blocks = soup.find_all('code')
    for block in code_blocks:
        new_tag = soup.new_tag("code")
        new_tag['class'] = "removed"
        block.replace_with(new_tag)

    markeddown = markdown.markdown(unicode(soup))

    # Replace the pulled code blocks with syntax-highlighted versions.
    markeddown = BeautifulSoup(markeddown, "html.parser")
    empty_code_blocks = markeddown.find_all('code', {'class':'removed'})
    index = 0
    formatter = HtmlFormatter(cssclass='highlight')
    for block in code_blocks:
        if block.has_key('class'):
            language = block['class'][0]
        else:
            language = 'text'
        try:
            lexer = get_lexer_by_name(language, stripnl=True, encoding='UTF-8')
        except ValueError, e:
            lexer = get_lexer_by_name('text', stripnl=True, encoding='UTF-8')

        code_highlight = highlight(unicode(block.string), lexer, formatter)
        tag_highlight = BeautifulSoup(code_highlight, 'html.parser')
        empty_code_blocks[index].replace_with(tag_highlight)
        index += 1

    return markeddown

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
