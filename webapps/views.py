import datetime

from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from webapps.models import WebAppInfo
from webapps.tools import send_mail, website_is_down, get_last_updated_id
from apps.twitcn.tools import getPrivateApi


def send_tweets_to_kindle(request):
    token = settings.TWITCN_PRIVATE_TOKEN
    api = getPrivateApi(token)
    #since_id = get_last_updated_id(api)
    since_id = "97961065496838145"
    latest_id = api.GetHomeTimeline(count=1)

    messages = api.GetHomeTimeline(since_id=since_id, count=5)
    while messages[-1].id < latest_id:
        since_id = messages[-1].id + 1
        messages += api.GetHomeTimeline(since_id=since_id, count=5)

    return render_to_response("twitcn/private.html", {'messages': messages,})


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

