from models import *
from django.contrib import admin

class ArticleAdmin(admin.ModelAdmin):
    fields = ('title', 'content', 'category')
    list_display = ('title', 'added', 'category')
    list_filter = ('category', )

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
