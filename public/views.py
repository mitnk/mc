from django.http import HttpResponse, Http404, HttpResponsePermanentRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from models import *

def index(request):
    articles = Article.objects.all()
    return render_to_response('blog/article_list.html', 
                              {'articles': articles,},
                              context_instance=RequestContext(request))

def linux_commands(request):
    command_list = UnixCommand.objects.all()
    return render_to_response('blog/linux_commands.html', 
                              {'command_list': command_list},
                              context_instance=RequestContext(request))

def about(request):
    return render_to_response('blog/about.html', 
                              context_instance=RequestContext(request))

def get_article(request, id, slug=None):
    try:
        article = Article.objects.get(id=id)
        url = article.get_absolute_url()
        if request.META["PATH_INFO"] != url:
            return HttpResponsePermanentRedirect(url)
        return render_to_response('blog/article.html',
                                  {'article': article, },
                                  context_instance=RequestContext(request))
    except Article.DoesNotExist:
        raise Http404

def get_tag(request, id):
    try:
        tag = Tag.objects.get(id=id)
        articles = tag.article_set.order_by("-added")
        return render_to_response('blog/article_list.html',
                                  {'tag': tag,
                                   'articles': articles,},
                                  context_instance=RequestContext(request))
    except Tag.DoesNotExist:
        raise Http404

def get_category(request, id):
    try:
        category = Category.objects.get(id=id)
        articles = category.article_set.order_by("-added")
        return render_to_response('blog/article_list.html',
                                  {'category': category,
                                   'articles': articles,},
                                  context_instance=RequestContext(request))
    except Category.DoesNotExist:
        raise Http404


def get_all_categories(request):
    categories = Category.objects.all()
    for category in categories:
        category.articles = category.article_set.order_by("-added")
    return render_to_response('blog/category.html', 
                              {'categories': categories, },
                              context_instance=RequestContext(request))

