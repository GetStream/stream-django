from django.db import models
from stream_django.activity import Activity


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
