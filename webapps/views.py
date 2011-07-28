import datetime

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from webapps.models import WebAppInfo
from webapps.tools import send_mail, website_is_down


@csrf_exempt
def check_website(request):
    content = "not check"
    if request.method == "POST":
        url = request.POST.get('url_for_check')
        site_name = request.POST.get('site_name')
        if not site_name or not site_name:
            return HttpResponse('params required')

        wai, created = WebAppInfo.objects.get_or_create(category='check_website', name=url)
        is_down = website_is_down(url)
        mail_to = ['wanghonggang@cn-acg.com']

        if is_down:
            # send means server is down and report email is sent
            if wai.value == 'send':
                # do nothing, just wait for rechecking
                content = "is down (had sent report)"
            else:
                wai.value = 'down'
                wai.save()

                content = "Target url: %s" % url
                content += "\r\nDown at: %s" % datetime.datetime.now()
                send_mail(mail_to, '%s is Down' % site_name, content)
                wai.value = 'send'
                wai.save()
        else:
            if not wai.value:
                wai.value = 'up'
                wai.save()

            if wai.value in ['down', 'send']:
                time_span = datetime.datetime.now() - wai.updated
                content = "Target url: %s" % url
                content += "\r\nUp at: %s" % datetime.datetime.now()
                content += "\r\nWas down for: %s" % time_span

                wai.value = 'up'
                wai.save()
                send_mail(mail_to, '%s is Up' % site_name, content)

    return HttpResponse(content)

