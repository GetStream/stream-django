from django.contrib.auth import get_user_model
from django.test import TestCase
import re
from test_app import models
import httpretty


api_url = re.compile(r'https://getstream.io/api/*.')


class PinTest(TestCase):

    def setUp(self):
        self.User = get_user_model()
        self.bogus = self.User.objects.create()

    @httpretty.activate
    def test_create(self):
        httpretty.register_uri(httpretty.POST, api_url,
              body='{}', status=200,
              content_type='application/json')
        pin = models.Pin.objects.create(author=self.bogus)
        last_req = httpretty.last_request()
        req_body = last_req.parsed_body
        self.assertEqual(req_body['foreign_id'], 'test_app.Pin:%s' % pin.id)
        self.assertEqual(req_body['object'], 'test_app.Pin:%s' % pin.id)
        self.assertEqual(req_body['verb'], 'pin')
        self.assertEqual(req_body['actor'], 'auth.User:%s' % self.bogus.id)

    @httpretty.activate
    def test_delete(self):
        httpretty.register_uri(httpretty.POST, api_url,
              body='{}', status=200,
              content_type='application/json')
        httpretty.register_uri(httpretty.DELETE, api_url,
              body='{}', status=200,
              content_type='application/json')
        pin = models.Pin.objects.create(author=self.bogus)
        pin.delete()
        last_req = httpretty.last_request()
        self.assertEqual(last_req.method, httpretty.DELETE)
