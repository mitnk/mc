#coding=utf-8
from django.conf import settings
from django.conf.urls.defaults import *
from views import *

_P = settings.PRIVATE_URL

urlpatterns = patterns('',
    (r'^$', index),
    (_P + r'$', private_tweet),
    (_P + r'm/$', private_mention),
    (_P + r're/$', private_retweets_of_me),
    (_P + r'dm/$', private_dm),
    (_P + r'f/$', private_favorites),
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
    (r'^tco/(\w+)', open_tco_url),
    (r'^more/', more),
    (r'^oauth/', login_with_oauth),
    (r'^callback/', callback),
    (r'^get_trends/', get_trends),

    # make sure user-page-url be the last one
    (r'^([0-9a-zA-Z_]+)/$', user_page),
)

