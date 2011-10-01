from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
    if request.user.is_authenticated():
        msg = "Welcom %s" % request.user
    else:
        msg = "Please login."
    return render_to_response('douqian/index.html', 
                              {'msg': msg,},
                              context_instance=RequestContext(request))

