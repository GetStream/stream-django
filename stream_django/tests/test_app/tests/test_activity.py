import unittest
from stream_django.activity import create_model_reference
from stream_django.activity import model_content_type
from stream_django.activity import create_reference
from stream_django.tests import Tweet


class ActivityTestCase(unittest.TestCase):

    def setUp(self):
        self.tweet = Tweet()
        self.tweet.id = 42
        self.tweet.actor = 'tommaso'

    def test_create_reference_to_model(self):
        data = 'not-a-model'
        ref = create_reference(data)
        self.assertEqual(ref, data)

    def test_activity_verb(self):
        activity = self.tweet.create_activity()
        self.assertEqual(activity['verb'], 'tweet')

    def test_activity_actor(self):
        activity = self.tweet.create_activity()
        self.assertEqual(activity['actor'], 'tommaso')

    def test_activity_object(self):
        activity = self.tweet.create_activity()
        self.assertEqual(activity['object'], 'stream_django.Tweet:42')

    def test_activity_notify(self):
        activity = self.tweet.create_activity()
        self.assertEqual(activity['to'], ['notification:thierry'])

    def test_activity_foreign_id(self):
        activity = self.tweet.create_activity()
        self.assertEqual(activity['foreign_id'], 'stream_django.Tweet:42')

    def test_create_reference(self):
        activity = self.tweet.create_activity()
        ref = create_model_reference(self.tweet)
        self.assertEqual(activity['foreign_id'], ref)

    def test_model_content_type(self):
        self.assertEqual(model_content_type(Tweet), 'stream_django.Tweet')
