from mitnkcom.public.models import Article, Category, Tag, UnixCommand
from mitnkcom.public.forms import ArticleForm
from django.contrib import admin

class ArticleAdmin(admin.ModelAdmin):
    search_fields = ['title', 'slug']
    list_display = ("title", "added")
    list_filter = ('added', 'tags')

    form = ArticleForm

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(UnixCommand)
