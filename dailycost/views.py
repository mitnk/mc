from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from dailycost.models import Cost, CostForm

def index(request):
    cs = Cost.objects.order_by("-added")[:5]
    this_month_cost = Cost.objects.get_this_month_cost()
    this_month_guess = Cost.objects.guess_this_month_total_cost()
    last_month_cost = Cost.objects.get_last_month_cost()
    if request.method == "POST":
        form = CostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("dailycost_index"))
    else:
        form = CostForm()
    return render_to_response('dailycost/index.html', 
                              {'cs': cs,
                               'this_month_cost': this_month_cost,
                               'this_month_guess': this_month_guess,
                               'last_month_cost': last_month_cost,
                               'form': form},
                              context_instance=RequestContext(request))

