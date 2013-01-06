from mitnkcom.wiki.models import Article
from django.contrib import admin

class ArticleAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ('title', 'added')

admin.site.register(Article, ArticleAdmin)
