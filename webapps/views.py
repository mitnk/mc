import datetime

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from webapps.models import WebAppInfo
from webapps.tools import send_mail, website_is_down


@csrf_exempt
def check_website(request):
    info = "not check"
    if request.method == "POST":
        url = request.POST.get('url_for_check')
        wai, created = WebAppInfo.objects.get_or_create(category='', name='')
        is_down = website_is_down(url)
        mail_to = ['wanghonggang@cn-acg.com']
        site_name = "Platform"

        if is_down:
            # send means server is down and report email is sent
            if wai.value == 'send':
                # do nothing, just wait for rechecking
                pass
            else:
                wai.value = 'down'
                wai.save()
                info = "checked: down."

                content = "Down at: %s" % datetime.datetime.now()
                send_mail(mail_to, '%s is Down' % site_name, content)
                wai.value = 'send'
                wai.save()
                info = "checked and sent: down."
        else:
            if wai.value in ['down', 'send']:
                time_span = datetime.datetime.now() - wai.updated
                content = "Up at: %s" % datetime.datetime.now()
                content += "\r\nWas down for: %s" % time_span
                info = "checked: up (again)."

                wai.value = 'up'
                wai.save()
                send_mail(mail_to, '%s is Up' % site_name, content)

    return HttpResponse("webapps.check_website - " + info)

