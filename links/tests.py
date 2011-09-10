from django.core.urlresolvers import reverse
from django.test import TestCase

class TestIndex(TestCase):
    def test_index(self):
        response = self.client.get(reverse("links"))
        self.assertEqual(response.status_code, 200)
