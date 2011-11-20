from models import *
from django.contrib import admin

class ArticleAdmin(admin.ModelAdmin):
    search_fields = ['title', 'slug']

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(UnixCommand)
