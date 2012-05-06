from models import *
from django.contrib import admin

class ArticleAdmin(admin.ModelAdmin):
    search_fields = ['title', 'slug']
    list_display = ("title", "added")
    list_filter = ('added', 'category')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(UnixCommand)
