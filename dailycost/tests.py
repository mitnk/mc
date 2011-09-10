from django.test import TestCase
from django.core.urlresolvers import reverse
from dailycost.models import Cost


class SimpleTest(TestCase):
    def test_model(self):
        c = Cost(amount=126, comment="mbp")
        c.save()
        self.assertEqual(Cost.objects.all().count(), 1)

class Test200URL(TestCase):
    def test_200(self):
        response = self.client.get(reverse("dailycost_index"))
        self.assertEqual(response.status_code, 200)
