from django.contrib import admin
from webapps.news.models import News


class NewsAdmin(admin.ModelAdmin):
    search_fields = ['title', 'url']
    list_display = ("title", "points", "added", 'filed')
    list_filter = ('added', 'filed')

admin.site.register(News, NewsAdmin)
