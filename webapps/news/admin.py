from django.contrib import admin
from webapps.news.models import News, Archive


class NewsAdmin(admin.ModelAdmin):
    search_fields = ['title', 'url']

class ArchiveAdmin(admin.ModelAdmin):
    search_fields = ['file_name', 'url']

admin.site.register(News, NewsAdmin)
admin.site.register(Archive, ArchiveAdmin)
