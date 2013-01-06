from django.shortcuts import render, get_object_or_404
from mitnkcom.wiki.models import Article

def index(request):
    articles = Article.objects.order_by("-added")
    return render(request, 'wiki/article_list.html', {'articles': articles})

def get_article(request, aid):
    article = get_object_or_404(Article, pk=aid)
    return render(request, 'wiki/article.html', {'article': article})
