from django.contrib.auth import get_user_model
from django.test import TestCase
import re
from test_app import models
import httpretty
from stream_django.enrich import Enrich
from stream_django.feed_manager import feed_manager


api_url = re.compile(r'(us-east-api.)?stream-io-api.com(/api)?/*.')


class PinTest(TestCase):

    def setUp(self):
        feed_manager.enable_model_tracking()
        self.User = get_user_model()
        self.bogus = self.User.objects.create()
        self.enricher = Enrich()

    def register_post_api(self):
        httpretty.register_uri(httpretty.POST, api_url,
              body='{}', status=200,
              content_type='application/json')

    def register_delete_api(self):
        httpretty.register_uri(httpretty.DELETE, api_url,
              body='{}', status=200,
              content_type='application/json')

    @httpretty.activate
    def test_create(self):
        self.register_post_api()
        pin = models.Pin.objects.create(author=self.bogus)
        last_req = httpretty.last_request()
        req_body = last_req.parsed_body
        self.assertEqual(req_body['foreign_id'], 'test_app.Pin:%s' % pin.id)
        self.assertEqual(req_body['object'], 'test_app.Pin:%s' % pin.id)
        self.assertEqual(req_body['verb'], 'pin')
        self.assertEqual(req_body['actor'], 'auth.User:%s' % self.bogus.id)

    @httpretty.activate
    def test_delete(self):
        self.register_post_api()
        self.register_delete_api()
        pin = models.Pin.objects.create(author=self.bogus)
        pin.delete()
        last_req = httpretty.last_request()
        self.assertEqual(last_req.method, httpretty.DELETE)

    @httpretty.activate
    def test_enrich_instance(self):
        self.register_post_api()
        pin = models.Pin.objects.create(author=self.bogus)
        pin.save()
        activity = pin.create_activity()

        enriched_data = self.enricher.enrich_activities([activity])
        # check object field
        self.assertEqual(enriched_data[0]['object'].id, pin.id)
        self.assertIsInstance(enriched_data[0]['object'], models.Pin)
        # check actor field
        self.assertEqual(enriched_data[0]['actor'].id, pin.author_id)
        self.assertIsInstance(enriched_data[0]['actor'], self.User)

    @httpretty.activate
    def test_enrich_data_with_missing_reference(self):
        self.register_post_api()
        self.register_delete_api()
        pin = models.Pin.objects.create(author=self.bogus)
        pin.save()
        activity = pin.create_activity()
        pin.delete()
        # make sure missing data is correctly tracked
        enriched_data = self.enricher.enrich_activities([activity])
        self.assertFalse(enriched_data[0].enriched)
        self.assertIn('object', enriched_data[0].not_enriched_data)
        self.assertDictContainsSubset(dict(object=activity['object']), enriched_data[0].not_enriched_data)
        self.assertEqual(activity['object'], enriched_data[0]['object'])

    def test_disabled_tracking(self):
        feed_manager.disable_model_tracking()
        pin = models.Pin.objects.create(author=self.bogus)
        pin.save()
        pin.delete()
