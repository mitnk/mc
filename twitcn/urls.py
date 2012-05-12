#coding=utf-8
from django.conf import settings
from django.conf.urls import patterns, url
from views import *

_P = settings.TWITCN_PRIVATE_URL

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^' + _P + '/$', private_tweets, name="private_tweets"),
    url(r'^' + _P + '/c/$', private_clear_session),
    url(r'^' + _P + '/m/$', private_mention),
    url(r'^' + _P + '/f/$', private_favorites),
    url(r'^' + _P + '/re/$', private_retweets_of_me),
    url(r'^' + _P + '/dm/$', private_dm),
    url(r'^create_favorite/', create_favorite),
    url(r'^destroy_favorite/', destroy_favorite),
    url(r'^destroy_tweet/', destroy_tweet),
    url(r'^destroy_dm/', destroy_dm),
    url(r'^retweet/', retweet),
    url(r'^logout/', logout),
    url(r'^tweet/', tweet),
    url(r'^follow/', follow),
    url(r'^unfollow/', unfollow),
    url(r'^block/', block),
    url(r'^unblock/', unblock),
    url(r'^report_spam/', report_spam),
    url(r'^profile/', profile),
    url(r'^tco/(\w+)', open_tco_url),
    url(r'^more/', more),
    url(r'^oauth/', login_with_oauth),
    url(r'^callback/', callback),
    url(r'^get_trends/', get_trends),

    # make sure user-page-url be the last one
    url(r'^([0-9a-zA-Z_]+)/$', user_page),
)

