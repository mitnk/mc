#coding=utf-8
from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    (r'^$', index),
    (r'^p/$', private),
    (r'^create_favorite/', create_favorite),
    (r'^destroy_favorite/', destroy_favorite),
    (r'^destroy_tweet/', destroy_tweet),
    (r'^destroy_dm/', destroy_dm),
    (r'^retweet/', retweet),
    (r'^logout/', logout),
    (r'^tweet/', tweet),
    (r'^follow/', follow),
    (r'^unfollow/', unfollow),
    (r'^block/', block),
    (r'^unblock/', unblock),
    (r'^report_spam/', report_spam),
    (r'^profile/', profile),
    (r'^bitly/(\w+)', open_bitly_url),
    (r'^more/', more),
    (r'^oauth/', login_with_oauth),
    (r'^callback/', callback),
    (r'^get_trends/', get_trends),

    # make sure user-page-url be the last one
    (r'^([0-9a-zA-Z_]+)/$', user_page),
)

