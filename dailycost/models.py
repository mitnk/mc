import datetime

from django.db import models
from django.forms import ModelForm

from common.utils import get_1st_of_last_month

class CostManager(models.Manager):
    def get_last_month_cost(self, date_from=None):
        last_month = get_1st_of_last_month(date_from=date_from)
        cs = self.filter(added__month=last_month.month)
        return "%.2f" % sum([x.amount for x in cs])

    def get_this_month_cost(self, date_from=None):
        today = date_from or datetime.date.today()
        cs = self.filter(added__month=today.month)
        return "%.2f" % sum([x.amount for x in cs])

    def guess_this_month_total_cost(self, date_from=None):
        today = date_from or datetime.date.today()
        cs = self.filter(added__month=today.month)
        total = sum([x.amount for x in cs if x.amount < 1000])
        bigs = self.filter(added__month=today.month, amount__gte=1000)
        return "%.2f" % ((total / today.day) * 30 + sum([x.amount for x in bigs]))


class Cost(models.Model):
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    comment = models.CharField(max_length=40, null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)

    objects = CostManager()

    def __unicode__(self):
        return "Cost:%s at %s" % (self.amount, self.added)


class CostForm(ModelForm):
    class Meta:
        model = Cost
