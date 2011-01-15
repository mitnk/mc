from django import template
from django.conf import settings

register = template.Library()

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
