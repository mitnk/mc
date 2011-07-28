from django.template import RequestContext
from django.shortcuts import render_to_response
from models import Link

def index(request):
    links = Link.objects.all()
    return render_to_response('links.html', 
                              {'links': links,},
                              context_instance=RequestContext(request))

