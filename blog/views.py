from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from models import Article, Category

def index(request):
    articles = Article.objects.order_by("-added")
    return render_to_response('blog/article_list.html', 
                              {'articles': articles,},
                              context_instance=RequestContext(request))

def get_article(request, id):
    article = Article.objects.get(id=id)
    return render_to_response('blog/article.html',
                              {'article': article, },
                              context_instance=RequestContext(request))
