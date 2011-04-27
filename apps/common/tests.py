from django.test import TestCase

from apps.common.templatetags.common_tags import get_first_path
from apps.common.templatetags.common_tags import pygmentize

__test__ = {'test_get_first_path': get_first_path,
            'test_pygmentize': pygmentize,}

class TestPreinstalledLib(TestCase):
    def test_libs(self):
        import pygments
        import httplib2

class TestContextProcessors(TestCase):
    def test_request(self):
        response = self.client.get('/')
        self.assertTrue('request' in response.context)
        self.assertEqual(response.context['request'].META['PATH_INFO'], '/')
