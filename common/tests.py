import datetime

from django.test import TestCase

from common.utils import get_1st_of_last_month


class TestPreinstalledLib(TestCase):
    def test_libs(self):
        import pygments
        import httplib2

class TestContextProcessors(TestCase):
    def test_request(self):
        response = self.client.get('/')
        self.assertTrue('request' in response.context)
        self.assertEqual(response.context['request'].META['PATH_INFO'], '/')

class TestUtils(TestCase):
    def test_get_1st_of_last_month(self):
        d = get_1st_of_last_month(date_from=datetime.date(2011, 9, 14))
        self.assertEqual(d, datetime.date(2011, 8, 1))
        d = get_1st_of_last_month(date_from=datetime.date(2011, 1, 14))
        self.assertEqual(d, datetime.date(2010, 12, 1))

