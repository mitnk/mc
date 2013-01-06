import markdown
import re

from bs4 import BeautifulSoup
from django import template
from pygments import lexers, formatters, formatters, highlight

from mitnkcom.english.basic import basic_words

_lexer_names = reduce(lambda a,b: a + b[2], lexers.LEXERS.itervalues(), ())
_formatter = formatters.HtmlFormatter(cssclass='highlight')

register = template.Library()

@register.filter
def pygments_markdown(content):
    html = markdown.markdown(content)
    # Using html.parser to prevent bs4 adding <html> tags
    soup = BeautifulSoup(html, 'html.parser')
    for pre in soup.findAll('pre'):
        if pre.code:
            txt = unicode(pre.code.get_text())
            lexer_name = "text"
            if txt.startswith(':::'):
                lexer_name, txt = txt.split('\n', 1)
                lexer_name = lexer_name.split(':::')[1]

            if lexer_name not in _lexer_names:
                lexer_name = "text"
            lexer = lexers.get_lexer_by_name(lexer_name, stripnl=True, encoding='UTF-8')
            highlighted = highlight(txt, lexer, _formatter)
            div_code = BeautifulSoup(highlighted).div
            if not div_code:
                return content
            pre.replace_with(div_code)
    return unicode(soup)

def ParseWordProc(res):
    reply = res.group('word')
    if reply in basic_words:
        return reply
    return '<a href="/dict/%s/">%s</a>' % (reply, reply)

@register.filter
def lookup_words(text):
    p = re.compile(r'(?P<word>\w{4,})', re.VERBOSE)
    text = p.sub(ParseWordProc, text)
    return text
