from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from dailycost.models import Cost, CostForm

def index(request):
    cs = Cost.objects.order_by("-added")[:10]
    if request.method == "POST":
        form = CostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("dailycost_index"))
    else:
        form = CostForm()
    return render_to_response('dailycost/index.html', 
                              {'cs': cs,
                               'form': form},
                              context_instance=RequestContext(request))

