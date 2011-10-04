# encoding: UTF-8
from cgi import parse_qs

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from douqian import pydouban
from douqian.models import User, Book, Read
from douqian.utils import get_api, get_reading

def index(request):
    readings = get_reading(request)
    return render_to_response('douqian/index.html', 
                              {'readings': readings},
                              context_instance=RequestContext(request))


def read_detail(request, read_id):
    read = Read.objects.get(pk=read_id)
    return render_to_response('douqian/book.html', 
                              {'read': read},
                              context_instance=RequestContext(request))
    
def read_edit(request, read_id):
    read = Read.objects.get(id=read_id)
    if request.method == "POST":
        total = request.POST.get("total_page")
        if total:
            read.total = int(total)
            read.save()
        current = request.POST.get("page_current")
        if current:
            read.current = int(current)
            read.save()
        return HttpResponseRedirect(read.get_absolute_url())
    return render_to_response('douqian/read.html', 
                              {'read': read,},
                              context_instance=RequestContext(request))

def douban_callback(request):
    request_key = request.GET.get("oauth_token")
    request_secret = request.session.get("request_secret")
    auth = pydouban.Auth(key=settings.DOUBAN_API_KEY, secret=settings.DOUBAN_SECRET)
    try:
        access_tokens = auth.get_acs_token(request_key, request_secret)
        tokens = parse_qs(access_tokens)
        request.session["oauth_token"] = tokens["oauth_token"][0]
        request.session["oauth_token_secret"] = tokens["oauth_token_secret"][0]
        request.session["douban_user_id"] = tokens["douban_user_id"][0]
    except Exception, e:
        return HttpResponseRedirect(reverse("douqian_index"))

    # Create a user if not exist
    douban_id = request.session['douban_user_id']
    user, created = User.objects.get_or_create(douban_id=douban_id)
    if not user.name:
        api = get_api(request)
        people = api.get_people(user.douban_id)
        user.name = people['title']['t']
        user.save()

    if "request_secret" in request.session:
        del request.session["request_secret"]
    return HttpResponseRedirect(reverse("douqian_index"))


def logout(request):
    if "oauth_token" in request.session:
        del request.session["oauth_token"]
    if "oauth_token_secret" in request.session:
        del request.session["oauth_token_secret"]
    if "douban_user_id" in request.session:
        del request.session["douban_user_id"]
    if "request_secret" in request.session:
        del request.session["request_secret"]
    return HttpResponseRedirect(reverse("douqian_index"))


def login_with_douban(request):
    auth = pydouban.Auth(key=settings.DOUBAN_API_KEY, secret=settings.DOUBAN_SECRET)
    callback_url = "http://%s%s" % (request.META["HTTP_HOST"], reverse("douban_callback"))
    dic = auth.login(callback=callback_url)
    key, secret = dic['oauth_token'], dic['oauth_token_secret']
    request.session["request_secret"] = secret
    return HttpResponseRedirect(dic['url'])
