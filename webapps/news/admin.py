from django.contrib import admin
from webapps.news.models import News, Archive


class NewsAdmin(admin.ModelAdmin):
    search_fields = ['title', 'url']
    list_display = ("title", "url", "points", "added")
    list_filter = ('added',)

class ArchiveAdmin(admin.ModelAdmin):
    search_fields = ['file_name', 'url']
    list_display = ("file_name", "url", "added")
    list_filter = ('added',)

admin.site.register(News, NewsAdmin)
admin.site.register(Archive, ArchiveAdmin)
