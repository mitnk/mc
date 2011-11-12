from models import *
from django.contrib import admin
from webapps.models import FavoTweet

class ArticleAdmin(admin.ModelAdmin):
    fields = ('title', 'content', 'category')
    list_display = ('title', 'added', 'category')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(FavoTweet)
