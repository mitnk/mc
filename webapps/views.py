import datetime
import os.path
import rfc822
from urllib2 import HTTPError

from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt

from mitnkcom.webapps.models import WebAppInfo, FavoTweet, MyTweet
from mitnkcom.utils.mail import GSMTP
from mitnkcom.twitcn.tools import getPrivateApi


def index(request):
    return render_to_response("webapps/index.html")

@csrf_exempt
def favo_tweets(request):
    if request.method == "POST":
        token = settings.TWITCN_PRIVATE_TOKEN
        api = getPrivateApi(token)
        info = "blank"
        if request.POST.get('action') == "save":
            messages = api.GetFavorites()
            count = 0
            for message in messages:
                api.DestroyFavorite(message.id)
                added = datetime.datetime(*rfc822.parsedate(message.created_at)[:6])
                FavoTweet.objects.create(name=message.user.screen_name, 
                                         text=smart_str(message.text), 
                                         tweet_id=message.id, 
                                         added=added)
                count += 1
            info = "%s\n" % count
        return HttpResponse(info)

    messages = FavoTweet.objects.all()
    return render_to_response("webapps/favo_tweets.html",
        {'messages': messages},
        context_instance=RequestContext(request))

@csrf_exempt
def my_tweets(request):
    if request.method == "POST":
        token = settings.TWITCN_PRIVATE_TOKEN
        api = getPrivateApi(token)
        info = "blank"
        if request.POST.get('action') == "save":
            max_id = request.POST.get('max_id', None)
            messages = api.GetUserTimeline(user='mitnk', max_id=max_id, count=50)
            count = 0
            for message in messages:
                if message.text[0] == "@" or \
                    MyTweet.objects.filter(tweet_id=message.id).count() > 0:
                    continue
                added = datetime.datetime(*rfc822.parsedate(message.created_at)[:6])
                MyTweet.objects.create(name=message.user.screen_name, 
                                       text=smart_str(message.text), 
                                       tweet_id=message.id, 
                                       added=added)
                count += 1
            info = "%s\n" % count
        return HttpResponse(info)

    messages = MyTweet.objects.filter(added__year=datetime.date.today().year)
    return render_to_response("webapps/favo_tweets.html",
        {'messages': messages},
        context_instance=RequestContext(request))


def ckeditor(request):
    return render_to_response("webapps/ckeditor.html")

def get_last_updated_id():
    wai, created = WebAppInfo.objects.get_or_create(category='twitter', name="last_updated_id")
    if not created:
        return int(wai.value)
    return 0

def set_last_updated_id(latest_id):
    wai, created = WebAppInfo.objects.get_or_create(category='twitter', name="last_updated_id")
    wai.value = str(latest_id)
    wai.save()

@csrf_exempt
def send_tweets_to_kindle(request):
    if request.method != "POST":
        return HttpResponse("GET is not the right way.")

    count_limit = request.POST.get("count_limit")
    if not count_limit:
        return HttpResponse("No Count info provided.")

    try:
        count_limit = int(count_limit)
    except ValueError:
        return HttpResponse("Numbers needed.")

    STEP = 50
    token = settings.TWITCN_PRIVATE_TOKEN
    api = getPrivateApi(token)
    latest_id = get_last_updated_id()

    try:
        messages = api.GetHomeTimeline(count=STEP)
    except HTTPError, e:
        return HttpResponse("%s" % e)

    min_id = messages[-1].id - 1
    while latest_id and min_id > int(latest_id):
        messages += api.GetHomeTimeline(max_id=min_id, count=STEP)
        min_id = messages[-1].id - 1
        if len(messages) >= 500:
            break

    if latest_id:
        unread_number = 0
        for msg in messages:
            if msg.id > latest_id:
                unread_number += 1
            else:
                break
        messages = messages[:unread_number]

    # Do not send if too faw tweets
    if len(messages) < count_limit:
        return HttpResponse("Too faw tweets (%s/%s)" %(len(messages), count_limit))

    messages.reverse()
    for msg in messages:
        msg.text = smart_str(msg.text)
    content = render_to_string("webapps/tweets_for_kindle.txt", {'messages': messages})
    file_name = "Tweets_%s.txt" % datetime.datetime.now().strftime("%h-%d-%H-%M")
    file_name = os.path.join(settings.ZONGHENG_DIR, file_name)
    f = open(file_name, "w")
    f.write(smart_str(content))
    f.close()

    send_to = [settings.MY_KINDLE_MAIL,]
    subject = "Tweets Daily Update"
    text = "There are %s tweets updated." % len(messages)
    files = [file_name]
    stmp = GSMTP(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    stmp.send_mail(send_to, subject, text, files=files)
    set_last_updated_id(messages[-1].id)
    return HttpResponse("Sent %s tweets." % len(messages))

def http_meta(request):
    return render_to_response('webapps/http_meta.html',
                              context_instance=RequestContext(request))
