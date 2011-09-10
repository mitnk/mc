from django.test import TestCase
from dailycost.models import Cost


class SimpleTest(TestCase):
    def test_basic(self):
        c = Cost(amount=126, comment="mbp")
        c.save()
        self.assertEqual(Cost.objects.all().count(), 1)
