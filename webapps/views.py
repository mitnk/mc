import datetime
import os.path

from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt

from webapps.models import WebAppInfo
from webapps.tools import send_mail, website_is_down
from twitcn.tools import getPrivateApi

def index(request):
    return render_to_response("webapps/index.html")

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

def send_tweets_to_kindle(request):
    if request.method != POST:
        return HttpResponse("GET is not the right way.")

    COUNT_LIMIT = request.POST.get("count_limit"):
    if not COUNT_LIMIT:
        return HttpResponse("No Count info provided.")

    STEP = 100
    token = settings.TWITCN_PRIVATE_TOKEN
    api = getPrivateApi(token)
    latest_id = get_last_updated_id()

    messages = api.GetHomeTimeline(count=STEP)

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
    if len(messages) < 200:
        return HttpResponse("Too faw tweets")

    messages.reverse()
    for msg in messages:
        msg.text = smart_str(msg.text)
    content = render_to_string("webapps/tweets_for_kindle.txt", {'messages': messages})
    file_name = "Tweets_%s.txt" % datetime.datetime.now().strftime("%h-%d-%H-%M")
    file_name = os.path.join(settings.ZONGHENG_DIR, file_name)
    f = open(file_name, "w")
    f.write(smart_str(content))
    f.close()

    send_to = ['whgking@free.kindle.com']
    subject = "Tweets Daily Update"
    text = "There are %s tweets updated." % len(messages)
    files = [file_name]
    send_mail(send_to, subject, text, files=files, fail_silently=False)
    set_last_updated_id(messages[-1].id)
    return HttpResponse("Sent %s tweets." % len(messages))

@csrf_exempt
def check_website(request):
    content = "not check"
    if request.method == "POST":
        url = request.POST.get('url_for_check')
        site_name = request.POST.get('site_name')
        if not site_name or not site_name:
            return HttpResponse('params required')

        wai, created = WebAppInfo.objects.get_or_create(category='check_website', name=url)
        is_down, reason = website_is_down(url)
        if is_down:
            # check again to make sure it is really down
            is_down, reason = website_is_down(url)

        mail_to = ['wanghonggang@cn-acg.com']

        if is_down:
            # send means server is down and report email is sent
            if wai.value == 'send':
                # do nothing, just wait for rechecking
                content = "is down (had sent report)"
            else:
                # If server is already down, do not save to update the time again.
                if wai.value != 'down':
                    wai.value = 'down'
                    wai.save()

                content = "Target url: %s" % url
                content += "\r\nReason: %s" % reason
                content += "\r\nDown at: %s" % datetime.datetime.now()
                send_mail(mail_to, '%s is Down' % site_name, content, fail_silently=False)
                wai.value = 'send'
                wai.save()
        else:
            if not wai.value:
                wai.value = 'up'
                wai.save()

            if wai.value in ['down', 'send']:
                time_span = datetime.datetime.now() - wai.updated
                content = "Target url: %s" % url
                content += "\r\nReason: %s" % reason
                content += "\r\nUp at: %s" % datetime.datetime.now()
                content += "\r\nWas down for: %s" % time_span

                send_mail(mail_to, '%s is Up' % site_name, content, fail_silently=False)
                wai.value = 'up'
                wai.save()

    return HttpResponse(content)

def user_agent(request):
    if "HTTP_USER_AGENT" in request.META:
        return HttpResponse("-" + request.META["HTTP_USER_AGENT"] + "-\r\n")
    return HttpResponse("User-Agent not found.")
