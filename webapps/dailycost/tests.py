import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse

from webapps.dailycost.models import Cost


class Test200URL(TestCase):
    def test_200(self):
        response = self.client.get(reverse("dailycost_index"))
        self.assertEqual(response.status_code, 200)

class TestCostModel(TestCase):
    def test_model(self):
        Cost.objects.create(amount=126, comment="mbp")
        Cost.objects.create(amount=12)
        self.assertEqual(Cost.objects.all().count(), 2)

    def test_get_last_month_cost(self):
        c = Cost.objects.create(amount="2", comment="mbp")
        c.added = datetime.date(2011, 8, 1)
        c.save()
        self.assertEqual(c.added.month, 8)

        c = Cost.objects.create(amount="3")
        c.added = datetime.date(2011, 8, 7)
        c.save()
        c = Cost.objects.create(amount="5.35", comment="mbp")
        c.added = datetime.date(2011, 8, 21)
        c.save()
        c = Cost.objects.create(amount=5)
        c.added = datetime.date(2011, 9, 1)
        c.save()
        lmc = Cost.objects.get_last_month_cost(date_from=datetime.date(2011, 9, 7))
        self.assertEqual(lmc, "10.35")

    def test_get_this_month_cost(self):
        c = Cost.objects.create(amount="2", comment="shopping")
        c.added = datetime.date(2011, 8, 1)
        c.save()
        c = Cost.objects.create(amount="3")
        c.added = datetime.date(2011, 8, 7)
        c.save()
        c = Cost.objects.create(amount="5.35", comment="meal")
        c.added = datetime.date(2011, 8, 21)
        c.save()
        c = Cost.objects.create(amount=1000)
        c.added = datetime.date(2011, 8, 22)
        c.save()

        cost = Cost.objects.get_this_month_cost(date_from=datetime.date(2011, 8, 7))
        self.assertEqual(cost, "1010.35")

    def test_guess_this_month_total_cost(self):
        c = Cost.objects.create(amount="3", comment="shopping")
        c.added = datetime.date(2011, 8, 1)
        c.save()
        c = Cost.objects.create(amount="4")
        c.added = datetime.date(2011, 8, 7)
        c.save()
        c = Cost.objects.create(amount=1000)
        c.added = datetime.date(2011, 8, 2)
        c.save()

        cost = Cost.objects.guess_this_month_total_cost(date_from=datetime.date(2011, 8, 7))
        self.assertEqual(cost, "1030.00")
