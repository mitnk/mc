from models import *
from django.contrib import admin
from webapps.models import FavoTweet

class FavoTweetAdmin(admin.ModelAdmin):
    list_display = ('name', 'text')

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(FavoTweet)
