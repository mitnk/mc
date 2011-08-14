from django.shortcuts import render_to_response
from django.template import RequestContext

def linux_commands(request):
    return render_to_response('linux_commands.html', 
                              context_instance=RequestContext(request))

def about(request):
    return render_to_response('about.html', 
                              context_instance=RequestContext(request))

