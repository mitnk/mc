from webapps.models import FavoTweet, MyTweet

class FavoTweetAdmin(admin.ModelAdmin):
    list_display = ('name', 'text')

class MyTweetAdmin(admin.ModelAdmin):
    list_display = ('name', 'text')

admin.site.register(FavoTweet, FavoTweetAdmin)
admin.site.register(MyTweet, MyTweetAdmin)
