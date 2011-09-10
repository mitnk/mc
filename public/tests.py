from django.core.urlresolvers import reverse
from django.test import TestCase

class TestIndex(TestCase):
    def test_index(self):
        response = self.client.get(reverse("public_index"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("public_all_category"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
