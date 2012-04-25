from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from mitnkcom.webapps.dailycost.models import Cost, CostForm

def index(request):
    cs = Cost.objects.order_by("-added")[:10]
    this_month_net = Cost.objects.get_this_month_net_cost()
    this_month_total = Cost.objects.get_this_month_cost()
    this_month_guess = Cost.objects.guess_this_month_total_cost()
    last_month_total = Cost.objects.get_last_month_cost()
    last_month_net = Cost.objects.get_last_month_net_cost()
    if request.method == "POST":
        form = CostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("dailycost_index"))
    else:
        form = CostForm()
    ua = request.META.get("HTTP_USER_AGENT", '').lower()
    veer = 'webos' in ua
    return render_to_response('webapps/dailycost/index.html', 
                              {'cs': cs,
                               'this_month_net': this_month_net,
                               'this_month_total': this_month_total,
                               'this_month_guess': this_month_guess,
                               'last_month_total': last_month_total,
                               'last_month_net': last_month_net,
                               'veer': veer,
                               'form': form},
                              context_instance=RequestContext(request))
