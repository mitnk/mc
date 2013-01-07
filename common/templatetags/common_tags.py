import markdown
import random
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

@register.tag('remember_this')
def remember_this(parser, token):
    return RememberThis()

class RememberThis(template.Node):
    def render(self, context):
        count = len(QUOTES)
        return QUOTES[random.randint(0, count-1)]

QUOTES = (
    "Care About Your Craft",
    "Think! About Your Work",
    "Provide Options, Don't Make Lame Excuses",
    "Don't Live with Broken Windows",
    "Be a Catalyst for Change",
    "Remember the Big Pictrue",
    "Make Quality a Requirements Issue",
    "Invest Regularly in Your Knowledge Protfolio",
    "Critically Analyze What You Read and Hear",
    "DRY",
    "It's Both What You Say and the Way You Say It",
    "Make It Easy to Reuse",
    "Eliminate Effects Between Unrelated Things",
    "There Are No Final Decisions",
    "Use Tracer Bullets to Find the Target",
    "Prototype to Learn",
    "Program Close to the Problem domain",
    "Estimate to Avoid Surprises",
    "Iterate the Schedule with the Code",
    "Keep Knowledge in Plain Text",
    "Use the Power of Command  Effects Between Unrelated Things",
    "There Are No Final Decisions",
    "Use Tracer Bullets to Find the Target",
    "Prototype to Learn",
    "Program Close to the Problem domain",
    "Estimate to Avoid Surprises",
    "Iterate the Schedule with the Code",
    "Keep Knowledge in Plain Text",
    "Use the Power of Command  Effects Between Unrelated Things",
    "There Are No Final Decisions",
    "Use Tracer Bullets to Find the Target",
    "Prototype to Learn",
    "Program Close to the Problem domain",
    "Estimate to Avoid Surprises",
    "Iterate the Schedule with the Code",
    "Keep Knowledge in Plain Text",
    "Fix the Problem, Not the Blame",
    "Don't Panic When Debuging",
    '"SELECT" Isn\'t Broken',
    "Don't Assume It - Prove It",
    "Wirte Code that Write code",
    "You Can't Write Perfect Software",
    "Design with Contracts",
    "Crash Early",
    "Use Assertions to Prevent the Impossible",
    "Use Exceptions for Exceptions Problems",
    "Finish What You Start",
    "Minimize Coupling Between Modules",
    "Configure, Don't Integrate",
    "Put Abstractions in Code, Details in Metadata",
    "Analyze Workflow to Improve Concurrency",
    "Design Using Service",
    "Always Design for Concurrency",
    "Separate Views from Models",
    "Use Blackboards to Coordinate Workflow",
    "Test Your Estimates",
    "Refactor Early, Refactor Often",
    "Design to Test",
    "Test Your Software, or Your Users Will",
    "Don't Gather Requirements - Dig for Them",
    "Work with a User to Think Like a User",
    "Abstractions Live Longer than Details",
    "Use a Project Gloosary",
    "Don't Think Outside the Box - Find the Box",
    "Start When You're Ready",
    "Some Things Are Better Done than Described",
    "Don't Be a Slave to Formal Methods",
    "Costly Tools Don't Produce Better Designs",
    "Organize Teams Around Functionality",
    "Don't Use Manual Procedures",
    "Test Early. Test Often. Test Automatically",
    "Coding Ain't Done 'Til All the Tests Run",
    "Find Bugs Once",
    "English is Just a Programming Language",
    "Build Documentation In, Don't Bolt It On",
    "Gently Exceed Your Users' Expectations",
)
