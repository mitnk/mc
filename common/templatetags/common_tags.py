from bs4 import BeautifulSoup
import markdown
from pygments import lexers, formatters, formatters, highlight
from django import template

_lexer_names = reduce(lambda a,b: a + b[2], lexers.LEXERS.itervalues(), ())
_formatter = formatters.HtmlFormatter(cssclass='highlight')

register = template.Library()

@register.filter
def pygments_markdown(txt):
    html = markdown.markdown(txt)
    # Using html.parser to prevent bs4 adding <html> tags
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup.findAll('pre'):
        if tag.code:
            txt = unicode(tag.code.get_text())
            if txt.startswith('pygments:'):
                lexer_name, txt = txt.split('\n', 1)
                lexer_name = lexer_name.split(':')[1]
                if lexer_name in _lexer_names:
                    lexer = lexers.get_lexer_by_name(lexer_name, stripnl=True, encoding='UTF-8')
                    hl = highlight(txt, lexer, _formatter)
                    bhl = BeautifulSoup(hl)
                    tag.replace_with(bhl.div)

    return unicode(soup)
