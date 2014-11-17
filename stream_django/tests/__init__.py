from django.db import models
from stream_django.activity import Activity


class Tweet(Activity, models.Model):

    @property
    def activity_time(self):
        return None

    @property
    def activity_object_attr(self):
        return self

    @property
    def activity_actor(self):
        return self.actor

    @property
    def activity_notify(self):
        from stream_django.feed_manager import feed_manager
        return [feed_manager.get_notification_feed('thierry')]
