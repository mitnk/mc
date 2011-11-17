#coding=utf-8
import datetime
import re
from oauthtwitter import OAuthApi
from urllib2 import HTTPError
import twitter, oauth

from django.shortcuts import render_to_response
from django.http import *
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils import simplejson as json
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt

import requests

from tools import *
from asker_types import *

@csrf_exempt
def private_tweets(request):
    token = settings.TWITCN_PRIVATE_TOKEN
    api = getPrivateApi(token)
    if request.method == "POST":
        if request.POST.get("action") and request.POST.get("status_id"):
            if request.POST['action'] == "favo":
                api.CreateFavorite(request.POST["status_id"])
                return HttpResponse("ed")
            elif request.POST['action'] == "unfavo":
                api.DestroyFavorite(request.POST["status_id"])
                return HttpResponse("Favo")
            return HttpResponse("error")
        else:
            try:
                msg = request.POST.get("tweet_text")
                if not msg:
                    return HttpResponse("")

                in_reply_to_status_id = request.POST.get("in_reply_to_status_id") or None
                msg = shortenStatusUrls(msg)
                result = api.PostUpdates(msg, in_reply_to_status_id=in_reply_to_status_id)
                if isinstance(result[0], twitter.Status):
                    return render_to_response("twitcn/new_tweet.html", 
                                              {'status': result[0]},
                                              context_instance=RequestContext(request))
            except HTTPError, e:
                return HttpResponse("%s" % e)
            return HttpResponse("Post tweet failed")
    else:
        try:
            since_id = request.session.get('private_tweet_since_id', None)
            if since_id:
                messages = api.GetHomeTimeline(count=200, since_id=since_id)
                if not messages:
                    messages = api.GetHomeTimeline(count=1)
            else:
                messages = api.GetHomeTimeline(count=30)

            request.session['private_tweet_since_id'] = messages[0].id
        except HTTPError, e:
            return HttpResponse("%s" % e)
        ua = request.META.get("HTTP_USER_AGENT", '').lower()
        veer = (re.search(r'webos', ua) is not None)
        return render_to_response("twitcn/private.html", 
                                  {'messages': messages,
                                   'veer': veer,},
                                  context_instance=RequestContext(request))

def private_clear_session(request):
    if 'private_tweet_since_id' in request.session:
        del request.session['private_tweet_since_id']
    return HttpResponseRedirect(reverse('private_tweets'))

@csrf_exempt
def private_mention(request):
    if request.method == "POST":
        return private_tweets(request)

    token = settings.TWITCN_PRIVATE_TOKEN
    api = getPrivateApi(token)
    try:
        messages = api.GetMentions()
    except HTTPError, e:
        return HttpResponse("%s" % e)
    ua = request.META.get("HTTP_USER_AGENT", '').lower()
    veer = (re.search(r'webos', ua) is not None)
    return render_to_response("twitcn/private.html", 
                              {'messages': messages,
                               'veer': veer,},
                              context_instance=RequestContext(request))

@csrf_exempt
def private_favorites(request):
    token = settings.TWITCN_PRIVATE_TOKEN
    api = getPrivateApi(token)

    if request.method == "POST":
        if request.POST.get('action') == "save":
            messages = api.GetFavorites()
            for message in messages:
                api.DestroyFavorite(message.id)
                from webapps.models import FavoTweet
                import rfc822
                name = message.user.screen_name
                text = smart_str(message.text)
                added = datetime.datetime(*rfc822.parsedate(message.created_at)[:6])
                tweet_id = message.id
                FavoTweet.objects.create(name=name, text=text, tweet_id=tweet_id, added=added)
            return HttpResponse("%s\n" % len(messages))
        else:
            return private_tweets(request)

    try:
        messages = api.GetFavorites()
    except HTTPError, e:
        return HttpResponse("%s" % e)
    ua = request.META.get("HTTP_USER_AGENT", '').lower()
    veer = (re.search(r'webos', ua) is not None)
    return render_to_response("twitcn/private.html", 
                              {'messages': messages,
                               'veer': veer,},
                              context_instance=RequestContext(request))

@csrf_exempt
def private_dm(request):
    if request.method == "POST":
        return private_tweets(request)

    token = settings.TWITCN_PRIVATE_TOKEN
    api = getPrivateApi(token)
    try:
        messages = api.GetDirectMessages()
    except HTTPError, e:
        return HttpResponse("%s" % e)
    ua = request.META.get("HTTP_USER_AGENT", '').lower()
    veer = (re.search(r'webos', ua) is not None)
    return render_to_response("twitcn/private.html", 
                              {'messages': messages,
                               'veer': veer,},
                              context_instance=RequestContext(request))

def index(request):
    api, current_user = getTwitterApi(request, True)
    if not api:
        return render_to_response("twitcn/index_not_login.html",
                                  context_instance=RequestContext(request))
    lists = []
    try:
        lists = api.GetLists(current_user.screen_name)
        lists.extend(api.GetSubscriptionLists(current_user.screen_name))
    except:
        pass
        
    # 以下几个more_data_xxx_json传给页面内的Js当参数使用
    more_data_home = { "asker": ASKER_HOME }
    more_data_home["first_time"] = True
    more_data_home['page_name'] = "Home"
    more_data_home['cursor_name'] = "home_tab"
    more_data_home_json = json.dumps(more_data_home)

    more_data_auto_update = {"asker": ASKER_AUTOUPDATE}
    more_data_auto_update_json = json.dumps(more_data_auto_update)
    
    more_data_list = {'asker': ASKER_LIST}
    more_data_list['first_time'] = True
    for li in lists:
        more_data_list['page_name'] = li.full_name
        more_data_list['list_id'] = li.id
        more_data_list['list_user'] = li.user.screen_name
        more_data_list['cursor_name'] = "tab_" + str(li.id)
        li.more_data_json = json.dumps(more_data_list)
    
    more_data_messages = {'asker': ASKER_MESSAGES}
    more_data_messages['first_time'] = True
    more_data_messages['page_name'] = "Direct Messages"
    more_data_messages['cursor_name'] = "direct_messages_tab"
    more_data_messages_json = json.dumps(more_data_messages)

    
    more_data_mytweets = {'asker': ASKER_USER_PAGE}
    more_data_mytweets['first_time'] = True
    more_data_mytweets['aim_user_name'] =  current_user.screen_name
    more_data_mytweets['page_name'] = "My Tweets"
    more_data_mytweets['cursor_name'] = "mytweets_tab"
    more_data_mytweets_json = json.dumps(more_data_mytweets)
    
    more_data_help = {'asker': ASKER_HELP}
    more_data_help['first_time'] = True
    more_data_help['page_name'] = "About Twitcn"
    more_data_help_json = json.dumps(more_data_help)
    
    more_data_following = {'asker': ASKER_FOLLOWING}
    more_data_following['first_time'] = True
    more_data_following['page_name'] = "You follow " + str(current_user.friends_count) + " people"
    more_data_following_json = json.dumps(more_data_following)
    
    more_data_followers = {'asker': ASKER_FOLLOWER}
    more_data_followers['first_time'] = True
    more_data_followers['page_name'] = "Your " + str(current_user.followers_count) + " followers"
    more_data_followers_json = json.dumps(more_data_followers)
    
    more_data_mentions = {'asker': ASKER_MENTIONS}
    more_data_mentions['first_time'] = True
    more_data_mentions['page_name'] = "Tweets mentioning @" + current_user.screen_name
    more_data_mentions['cursor_name'] = "mentions_tab"
    more_data_mentions_json = json.dumps(more_data_mentions)
    
    more_data_retweets = {'asker': ASKER_RETWEETS}
    more_data_retweets['first_time'] = True
    more_data_retweets['page_name'] = "Retweets by friends"
    more_data_retweets['cursor_name'] = "retweets_tab"
    more_data_retweets_json = json.dumps(more_data_retweets)

    more_data_favorites = {'asker': ASKER_FAVORITES}
    more_data_favorites['favorite_page'] = 1
    more_data_favorites['first_time'] = True
    more_data_favorites['page_name'] = 'Favorites'
    more_data_favorites['cursor_name'] = "favorites_tab"
    more_data_favorites_json = json.dumps(more_data_favorites)

    return render_to_response("twitcn/index.html", 
                              {'current_user': current_user,
                               'lists': lists,
                               'page_name': "Home",
                               'more_data_help_json': more_data_help_json,
                               'more_data_home_json': more_data_home_json,
                               'more_data_auto_update_json': more_data_auto_update_json,
                               'more_data_messages_json': more_data_messages_json,
                               'more_data_mentions_json': more_data_mentions_json,
                               'more_data_retweets_json': more_data_retweets_json,
                               'more_data_mytweets_json': more_data_mytweets_json,
                               'more_data_favorites_json': more_data_favorites_json,
                               'more_data_following_json': more_data_following_json,
                               'more_data_followers_json': more_data_followers_json,},
                              context_instance=RequestContext(request))

def user_page(request, user_name):
    api, current_user = getTwitterApi(request)
    if not api or not current_user:
        return HttpResponseRedirect(get_root_path() + "/")
    
    aim_user = api.GetUser(user_name)
    
    aim_user.isBlocked = api.IsBlocked(user_id=aim_user.id)

    followings = []
    more_data = {'asker': ASKER_USER_PAGE }
    more_data['aim_user_name'] = aim_user.screen_name
    if aim_user.protected and not aim_user.following and not (user_name == current_user.screen_name):
        more_data['protected'] = True
    else:
        followings = api.GetFriends(user=user_name)
        followings = followings[:36]

    greater_than_36 = aim_user.followers_count > 36
        
    more_data['page_name'] = aim_user.screen_name
    more_data['first_time'] = True
    more_data['cursor_name'] = "tweets_tab"
    more_data_json = json.dumps(more_data)
    
    more_data_favorites = {'asker': ASKER_FAVORITES}
    more_data_favorites['favorite_page'] = 1
    more_data_favorites['aim_user_name'] = aim_user.screen_name
    more_data_favorites['first_time'] = True
    if aim_user.protected and not aim_user.following and not (user_name == current_user.screen_name):
        more_data_favorites['protected'] = True
    more_data_favorites['page_name'] = "@" + aim_user.screen_name + "'s Favorite Tweets"
    more_data_favorites['cursor_name'] = "favorites_tab"
    more_data_favorites_json = json.dumps(more_data_favorites)
    
    more_data_following = {'asker': ASKER_FOLLOWING}
    more_data_following['first_time'] = True
    more_data_following['user_name'] = aim_user.screen_name
    more_data_following['page_name'] = aim_user.screen_name + " follows " + str(aim_user.friends_count) + " people"
    more_data_following_json = json.dumps(more_data_following)
    
    more_data_help = {'asker': ASKER_HELP}
    more_data_help['first_time'] = True
    more_data_help['page_name'] = "About Twitcn"
    more_data_help_json = json.dumps(more_data_help)
    
    more_data_followers = {'asker': ASKER_FOLLOWER}
    more_data_followers['first_time'] = True
    more_data_followers['user_name'] = aim_user.screen_name
    more_data_followers['page_name'] = aim_user.screen_name + "'s " + str(aim_user.followers_count) + " followers"
    more_data_followers_json = json.dumps(more_data_followers)

    return render_to_response("twitcn/user_page.html", 
                              {'aim_user': aim_user,
                               'followings': followings,
                               'current_user': current_user,
                               'greater_than_36': greater_than_36,
                               'more_data_help_json': more_data_help_json,
                               'page_name': aim_user.screen_name,
                               'more_data_json': more_data_json,
                               'more_data_favorites_json': more_data_favorites_json,
                               'more_data_following_json': more_data_following_json,
                               'more_data_followers_json': more_data_followers_json,},
                               context_instance=RequestContext(request))


def tweet(request):
    if request.method == "POST":
        msg = request.POST.get("tweet-text")
        if msg:
            api, current_user = getTwitterApi(request)
            try:
                in_reply_to_status_id = request.POST.get("in_reply_to_status_id") or None
                msg = shortenStatusUrls(msg)
                result = api.PostUpdates(msg, in_reply_to_status_id=in_reply_to_status_id)
    
                if isinstance(result[0], twitter.Status):
                    return render_to_response("twitcn/my_new_post.html", 
                                              {'messages': result,
                                               'current_user': current_user,},
                                              context_instance=RequestContext(request))
                else:
                    return HttpResponse("TWITCNERROR: other")
            except Exception, e:
                return HttpResponse("TWITCNERROR: " + e.message)
    return HttpResponse("TWITCNERROR: PLZPOST")

def profile(request):
    api, current_user = getTwitterApi(request, True)
    if not api:
        HttpResponseRedirect(get_root_path() + "/")
    
    if request.method == "POST":
        name = request.POST.get("profile_name")
        location = request.POST.get("profile_location")
        url = request.POST.get("profile_url")
        bio = request.POST.get("profile_bio")
        
        if name:
            current_user.name = name
        elif location:
            current_user.location = location
        elif url:
            current_user.url = url
        elif bio:
            current_user.description = bio
            
        api.SetUserProfile(current_user)
        return HttpResponseRedirect(request.META.get("PATH_INFO"))
    
    return render_to_response("twitcn/profile.html",
                              {'current_user': current_user,},
                              context_instance=RequestContext(request))


def create_favorite(request):
    if request.method == "POST":
        status_id = request.POST.get("status_id")
        if status_id:
            api, current_user = getTwitterApi(request)

            api.CreateFavorite(status_id)
            return HttpResponse('ok|' + status_id)

    return HttpResponse('post, no get')

def retweet(request):
    if request.method == "POST":
        status_id = request.POST.get("status_id")
        if status_id:
            api, current_user = getTwitterApi(request)
            if not current_user:
                return HttpResponse('need login.')
            try:
                api.Retweet(status_id)
                return HttpResponse('ok|' + status_id)
            except Exception, e:
                return HttpResponse('Error:' + e.message)
    return HttpResponse('post, no get')

def destroy_favorite(request):
    if request.method == "POST":
        status_id = request.POST.get("status_id")
        if status_id:
            api, current_user = getTwitterApi(request)
            if not current_user:
                return HttpResponse('need login.')
            try:
                api.DestroyFavorite(status_id)
                return HttpResponse('ok|' + status_id)
            except Exception, e:
                return HttpResponse('Error:' + e.message)
    return HttpResponse('post, no get')

def get_trends(request):
    if request.method == "POST":
        flag = request.POST.get("flag")
        if not flag:
            return HttpReposne("need flag")
        
        trends = []
        try:
            api, current_user = getTwitterApi(request)
            if flag == "current":
                trends = api.GetTrends()
            else:
                trends = api.GetTrends(flag="daily")
        except:
            pass
            
        trend_index = 1
        more_data_search = {'asker': ASKER_SEARCH }
        more_data_search["first_time"] = True
        for trend in trends:
            more_data_search['page_name'] = "Real-time result for " + trend.name
            more_data_search['q'] = trend.name
            more_data_search['cursor_name'] = "trend_" + str(trend_index) + "_tab"
            trend.more_data_json = json.dumps(more_data_search)
            trend_index += 1
        return render_to_response("twitcn/trends.html", 
                                  {'trends': trends,},
                                   context_instance=RequestContext(request))
    return HttpReposne()

def destroy_dm(request):
    if request.method == "POST":
        status_id = request.POST.get("status_id")
        if status_id:
            api, current_user = getTwitterApi(request)
            if not current_user:
                return HttpResponse('need login.')
            api.DestroyDirectMessage(status_id)
            return HttpResponse('ok|' + status_id)
    return HttpResponse('post, no get')

def destroy_tweet(request):
    if request.method == "POST":
        status_id = request.POST.get("status_id")
        if status_id:
            api, current_user = getTwitterApi(request)
            if not current_user:
                return HttpResponse('need login.')
            api.DestroyStatus(status_id)
            return HttpResponse('ok|' + status_id)
    return HttpResponse('post, no get')

def block(request):
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        if user_name:
            api, current_user = getTwitterApi(request)
            if not current_user:
                return HttpResponse('need login.')
            try:
                api.Block(user_name)
                return HttpResponse('ok|' + user_name)
            except Exception, e:
                return HttpResponse('Error:' + e.message)
    return HttpResponse('post, no get')

def report_spam(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        if user_id:
            api, current_user = getTwitterApi(request)
            if not current_user:
                return HttpResponse('need login.')
            try:
                user = api.ReportSpam(user_id=user_id)
                return HttpResponse('ok|' + user.screen_name)
            except:
                pass
    return HttpResponse('post, no get')
    
def unblock(request):
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        if user_name:
            api, current_user = getTwitterApi(request)
            if not current_user:
                return HttpResponse('need login.')
            try:
                api.Unblock(user_name)
                return HttpResponse('ok|' + user_name)
            except:
                pass
    return HttpResponse('post, no get')
    
def follow(request):
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        if user_name:
            api, current_user = getTwitterApi(request)
            if not current_user:
                return HttpResponse('need login.')
            try:
                api.PostUpdates("follow " + user_name)
                return HttpResponse('ok|' + user_name)
            except Exception, e:
                return HttpResponse('Error:' + e.message)
    return HttpResponse('post, no get')


def unfollow(request):
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        if user_name:
            api, current_user = getTwitterApi(request)
            if not current_user:
                return HttpResponse('need login.')
            try:
                api.DestroyFriendship(user_name)
                return HttpResponse('ok|' + user_name)
            except:
                pass
    return HttpResponse('post, no get')
    

def open_tco_url(request, url_string):
    url = 'http://t.co/%s' % url_string
    return HttpResponseRedirect(requests.get(url, timeout=3).url or url)


def logout(request):
    if request.session.get('access_token'):
        del request.session["access_token"]
    if request.session.get('user_info'):
        del request.session["user_info"]
    return HttpResponsePermanentRedirect(get_root_path() + "/")

def login_with_oauth(request):
    api = OAuthApi(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    request_token = api.getRequestToken()
    request.session["request_token"] = request_token.to_string()
    authorization_url = api.getAuthorizationURL(request_token)
    return HttpResponseRedirect(authorization_url)
    
def callback(request):
    req_token = oauth.Token.from_string(request.session.get('request_token'))
    api = OAuthApi(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, req_token.key, req_token.secret)
    access_token = api.getAccessToken() 
    request.session["access_token"] = access_token.to_string()
    del request.session["request_token"]
    return HttpResponseRedirect(get_root_path() + "/")

def updateSinceIdForAutoUpdate(request, messages):
    if messages:
        if messages[0].retweeted_id:
            request.session["since_id_for_update"] = messages[0].retweeted_id + 1
        else:
            request.session["since_id_for_update"] = messages[0].id + 1


def more(request):
    """ Get Information (statuses, DM, followers etc.) for different pages """
    if request.method != "POST":
        return HttpResponse("Post, no get.")

    asker = request.POST.get('asker')
    if not asker:
        return HttpResponse("need asker")
    more_data = {'asker': asker}

    messages = []
    max_id = request.POST.get('max_id')
    api, current_user = getTwitterApi(request)

    info_tweet = {'id': 4784502101L, 
                         'source': u'<a href="http://twitcn.info">twitcn</a>', 
                         'text': u'Service does not available :-( Please try again.', 
                         'user': {'description': 'Hi, sorry to say this.', 
                                  'id':3502724, 
                                  'name': u'twit_cn', 
                                  'profile_image_url': u'http://a3.twimg.com/profile_images/502380531/twitcn_normal.jpg', 
                                  'screen_name': u'twit_cn', 'time_zone': u'Beijing', 
                                  'url': u'', 'utc_offset': 28800}
                        }

    ######## for home page ########
    if asker == ASKER_HOME:
        try:
            messages = api.GetHomeTimeline(max_id=max_id)
            if request.POST.get('first_time'):
                updateSinceIdForAutoUpdate(request, messages)

            if messages:
                max_id = messages[-1].id - 1
        except:
            messages = [info_tweet]
        
        more_data['max_id'] = str(max_id)
        more_data_json = json.dumps(more_data)
        return render_to_response("twitcn/more.html", 
                          {'current_user': current_user,
                           'more_data_json': more_data_json,
                           'messages': messages,},
                          context_instance=RequestContext(request))

    ######## for auto-update new tweets ########
    if asker == ASKER_AUTOUPDATE:
        since_id = request.session.get('since_id_for_update')
        if not since_id:
            return HttpResponse("need since_id.")

        try:
            messages = api.GetHomeTimeline(since_id=since_id, count=200)
            updateSinceIdForAutoUpdate(request, messages)
        except:
            return HttpResponse()
        return render_to_response("twitcn/more.html", 
                                  {'messages': messages,
                                   'auto_update': True,},
                                  context_instance=RequestContext(request))

    ######## for metiones page ########
    elif asker == ASKER_MENTIONS:
        try:
            messages = api.GetMentions(max_id=max_id)
            if messages:
                max_id = messages[-1].id - 1
        except:
            messages = [info_tweet]
        
        more_data['max_id'] = str(max_id)
        more_data_json = json.dumps(more_data)
        return render_to_response("twitcn/more.html", 
                          {'current_user': current_user,
                           'more_data_json': more_data_json,
                           'messages': messages,},
                          context_instance=RequestContext(request))

    ######## for retweets page ########
    elif asker == ASKER_RETWEETS:
        try:
            messages = api.GetRetweets(max_id=max_id)
            if messages:
                max_id = messages[-1].id - 1
        except:
            messages = [info_tweet]
        
        more_data['max_id'] = str(max_id)
        more_data_json = json.dumps(more_data)
        return render_to_response("twitcn/more.html", 
                          {'current_user': current_user,
                           'more_data_json': more_data_json,
                           'messages': messages,},
                          context_instance=RequestContext(request))

    ######## for direct messages page ########
    elif asker == ASKER_MESSAGES:
        try:
            messages = api.GetDirectMessages(max_id=max_id)
            if messages:
                max_id = messages[-1].id - 1
        except Exception, e:
            info_tweet['text'] = str(e)
            messages = [info_tweet]
        
        more_data['max_id'] = str(max_id)
        more_data_json = json.dumps(more_data)
        return render_to_response("twitcn/more_dm.html", 
                                  {'more_data_json': more_data_json,
                                   'messages': messages,},
                                  context_instance=RequestContext(request))

    ######## for favorites page ########
    elif asker == ASKER_FAVORITES:
        page = request.POST.get('favorite_page', 1)
        user_name = request.POST.get('aim_user_name', current_user.screen_name)
        protected = ( request.POST.get('protected') != None )
        
        if protected:
            more_data['protected'] = True
            info_tweet['text'] = u'This person has protected the tweets.'
            messages = [info_tweet]
        else:
            messages = api.GetFavorites(user=user_name, page=page)
            if messages:
                page = int(page) + 1
        
        more_data['favorite_page'] = page
        more_data['aim_user_name'] = user_name
        more_data_json = json.dumps(more_data)
        return render_to_response("twitcn/more.html", 
                                  {'current_user': current_user,
                                   'more_data_json': more_data_json,
                                   'protected': protected,
                                   'messages': messages,},
                                   context_instance=RequestContext(request))
            
    ######## for lists page ########
    elif asker == ASKER_LIST:
        list_id = request.POST.get('list_id')
        list_user = request.POST.get('list_user')
        if not list_id or not list_user:
            return HttpResponse("need list id and list user!")
        
        try:
            messages = api.GetListStatuses(list_id, user=list_user, max_id=max_id)
            if messages:
                max_id = messages[-1].id - 1
        except:
            messages = [info_tweet]
        
        more_data['list_id'] = list_id
        more_data['list_user'] = list_user
        more_data['max_id'] = str(max_id)
        more_data_json = json.dumps(more_data)
        return render_to_response("twitcn/more.html", 
                                  {'current_user': current_user,
                                   'more_data_json': more_data_json,
                                   'messages': messages,},
                                   context_instance=RequestContext(request))
            
    ######## for help page, dispaly twit_cn's favorites ########
    if asker == ASKER_HELP:
        page = request.POST.get('favorite_page', 1)
        try:
            messages = api.GetFavorites(user='twit_cn', page=page)
            if messages:
                page = int(page) + 1
        except:
            messages = [info_tweet]

        more_data['favorite_page'] = page
        more_data_json = json.dumps(more_data)
        return render_to_response("twitcn/more.html", 
                                  {'current_user': current_user,
                                   'more_data_json': more_data_json,
                                   'messages': messages,},
                                   context_instance=RequestContext(request))
        
    ######## Search tweets ########
    if asker == ASKER_SEARCH:
        from_bing = False
        page = request.POST.get('page', 1)
        q = request.POST.get('q')
        if not q:
            return HttpResponse("need query string!")
        
        try:
            messages = api.SearchTwitter(q, max_id=max_id)
            if messages:
                from_bing = not messages[0].source
                max_id = messages[-1].id - 1
                page = int(page) + 1
        except:
            info_tweet['text'] = u'Sorry, no results found.'
            messages = [info_tweet]

        more_data['q'] = q
        more_data['page'] = page
        more_data['max_id'] = str(max_id)
        more_data_json = json.dumps(more_data)
        return render_to_response("twitcn/more_search.html", 
                                  {'more_data_json': more_data_json,
                                   'from_bing': from_bing,
                                   'messages': messages,},
                                   context_instance=RequestContext(request))
    
    ######## tweets of user page ########
    elif asker == ASKER_USER_PAGE:
        the_first_time = not max_id
            
        aim_user_name = request.POST.get('aim_user_name')
        if not aim_user_name:
            return HttpResponse("need user name.")
        
        protected = ( request.POST.get('protected') != None )
        if protected:
            more_data['protected'] = True
            info_tweet['text'] = u'This person has protected the tweets.'
            messages = [info_tweet]
        else:
            messages = api.GetUserTimeline(user=aim_user_name, max_id=max_id)
            if messages: 
                max_id = messages[-1].id - 1
        
        more_data['aim_user_name'] =  aim_user_name
        more_data['max_id'] = str(max_id)
        more_data_json = json.dumps(more_data)
        return render_to_response("twitcn/more_user_page.html", 
                                  {'current_user': current_user,
                                   'more_data_json': more_data_json,
                                   'the_first_time': the_first_time,
                                   'protected': protected,
                                   'this_is_user_page': True,
                                   'messages': messages,},
                                   context_instance=RequestContext(request))

    ######## for following page ########
    elif asker == ASKER_FOLLOWING:
        user_name = request.POST.get('user_name')
        try:
            users = api.GetFriends(user=user_name)
        except:
            users = [info_tweet]
        
        more_data['next_cursor'] = None
        more_data['previous_cursor'] = None
        more_data['user_name'] = user_name
        more_data_json = json.dumps(more_data)
        
        return render_to_response("twitcn/more_follow.html", 
                                  {'more_data_json': more_data_json,
                                   'users': users,},
                                  context_instance=RequestContext(request))

    ######## for follower page ########
    elif asker == ASKER_FOLLOWER:
        user_name = request.POST.get('user_name')
        try:
            users = api.GetFollowers(user=user_name)
        except:
            users = [info_tweet]
        
        more_data['next_cursor'] = None
        more_data['previous_cursor'] = None
        more_data['user_name'] = user_name
        more_data_json = json.dumps(more_data)
        
        return render_to_response("twitcn/more_follow.html", 
                                  {'more_data_json': more_data_json,
                                   'users': users,},
                                  context_instance=RequestContext(request))

    #default return
    return HttpResponse()

