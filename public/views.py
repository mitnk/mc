from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from models import *

def index(request):
    articles = Article.objects.order_by("-added")
    return render_to_response('blog/article_list.html', 
                              {'articles': articles,},
                              context_instance=RequestContext(request))

def linux_commands(request):
    return render_to_response('blog/linux_commands.html', 
                              context_instance=RequestContext(request))

def about(request):
    return render_to_response('blog/about.html', 
                              context_instance=RequestContext(request))

def get_article(request, id):
    try:
        article = Article.objects.get(id=id)
        return render_to_response('blog/article.html',
                                  {'article': article, },
                                  context_instance=RequestContext(request))
    except Article.DoesNotExist:
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

