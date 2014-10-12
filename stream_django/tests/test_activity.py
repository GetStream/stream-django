import unittest
from stream_django.activity import Activity
from stream_django.activity import create_model_reference
from django.db import models


class Tweet(Activity, models.Model):

    @property
    def activity_time(self):
        return None

    @property
    def activity_actor(self):
        return self.actor

    @property
    def activity_notify(self):
        return ['thierry']


class ActivityTestCase(unittest.TestCase):

    def setUp(self):
        self.tweet = Tweet()
        self.tweet.id = 42
        self.tweet.actor = 'tommaso'

    def test_activity_verb(self):
        activity = self.tweet.create_activity()
        self.assertEqual(activity['verb'], 'tweet')

    def test_activity_actor(self):
        activity = self.tweet.create_activity()
        self.assertEqual(activity['actor'], 'tommaso')

    def test_activity_object(self):
        activity = self.tweet.create_activity()
        self.assertEqual(activity['object'], 'tests.Tweet:42')

    def test_activity_notify(self):
        activity = self.tweet.create_activity()
        self.assertEqual(activity['to'], ['thierry'])

    def test_activity_foreign_id(self):
        activity = self.tweet.create_activity()
        self.assertEqual(activity['foreign_id'], 'tests.Tweet:42')

    def test_activity_activity_template(self):
        self.assertEqual(self.tweet.activity_template, 'activity/tweet.html')

    def test_create_reference(self):
        activity = self.tweet.create_activity()
        ref = create_model_reference(self.tweet)
        self.assertEqual(activity['foreign_id'], ref)
