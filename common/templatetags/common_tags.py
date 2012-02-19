import re
import markdown
from pygments import highlight
from pygments.lexers import guess_lexer, get_lexer_by_name, BashLexer
from pygments.formatters import HtmlFormatter

from django import template
from django.conf import settings
from external_libs.BeautifulSoup import BeautifulSoup


register = template.Library()

@register.filter
def pygments_markdown(content):
    """Render this content for display."""
    # First, pull out all the <code></code> blocks, to keep them away
    # from Markdown (and preserve whitespace).
    soup = BeautifulSoup(content)
    code_blocks = soup.findAll('code')
    for block in code_blocks:
        block.replaceWith('<code class="removed"></code>')
    markeddown = markdown.markdown(unicode(soup))

    # Replace the pulled code blocks with syntax-highlighted versions.
    soup = BeautifulSoup(markeddown)
    empty_code_blocks, index = soup.findAll('code', 'removed'), 0
    formatter = HtmlFormatter(cssclass='highlight')
    for block in code_blocks:
        if block.has_key('class'):
            # <code class='python'>python code</code>
            language = block['class']
        else:
            # <code>plain text, whitespace-preserved</code>
            language = 'text'
        try:
            lexer = get_lexer_by_name(language, stripnl=True, encoding='UTF-8')
        except ValueError, e:
            try:
                # Guess a lexer by the contents of the block.
                lexer = guess_lexer(block.renderContents())
            except ValueError, e:
                # Just make it plain text.
                lexer = get_lexer_by_name('text', stripnl=True, encoding='UTF-8')
        empty_code_blocks[index].replaceWith(
                highlight(block.renderContents(), lexer, formatter))
        index = index + 1
    return soup

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
