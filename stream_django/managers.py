from django.db.models.signals import post_delete, post_save
from stream_django import conf
from stream_django.activity import Activity
from stream_django.client import stream_client


EVERY_MODEL = 'EVERY_MODEL'


class FeedManager(object):

    def __init__(self):
        self.notification_feed = conf.NOTIFICATION_FEED
        self.user_feed = conf.USER_FEED
        self.news_feeds = conf.NEWS_FEEDS
        self._disabledModelTracking = {}

    def disable_model_tracking(self, model=EVERY_MODEL):
        self._disabledModelTracking[model] = True

    def enable_model_tracking(self, model=EVERY_MODEL):
        self._disabledModelTracking[model] = False

    def get_user_feed(self, user_id, feed_type=None):
        if feed_type is None:
            feed_type = self.user_feed
        feed = stream_client.feed(feed_type, user_id)
        return feed

    def get_notification_feed(self, user_id):
        return stream_client.feed(self.notification_feed, user_id)

    def get_actor_feed(self, instance=None):
        if instance.activity_author_feed is not None:
            return instance.activity_author_feed
        else:
            return self.user_feed

    def follow_user(self, user_id, target_user_id):
        news_feeds = self.get_news_feeds(user_id)
        target_feed = self.get_user_feed(target_user_id)
        for feed in news_feeds.values():
            feed.follow(target_feed.slug, target_feed.user_id)

    def unfollow_user(self, user_id, target_user_id):
        news_feeds = self.get_news_feeds(user_id)
        target_feed = self.get_user_feed(target_user_id)
        for feed in news_feeds.values():
            feed.unfollow(target_feed.slug, target_feed.user_id)

    def get_feed(self, feed, user_id):
        return stream_client.feed(feed, user_id)

    def get_news_feeds(self, user_id):
        feeds = {}
        for feed in self.news_feeds:
            feeds[feed] = self.get_feed(feed, user_id)
        return feeds

    def add_activity_to_feed(self, instance):
        activity = instance.create_activity()
        feed_type = self.get_actor_feed(instance)
        feed = self.get_feed(feed_type, instance.activity_actor_id)
        result = feed.add_activity(activity)
        return result

    def remove_activity_from_feed(self, instance):
        feed_type = self.get_actor_feed(instance)
        feed = self.get_feed(feed_type, instance.activity_actor_id)
        result = feed.remove_activity(
            foreign_id=instance.activity_foreign_id)
        return result

    def should_track(self, model):
        disabled_all = conf.DISABLE_MODEL_TRACKING or self._disabledModelTracking.get(
            EVERY_MODEL)
        model_disabled = self._disabledModelTracking.get(model)
        return (not disabled_all and not model_disabled)

    def activity_created(self, sender, instance, created, raw, **kwargs):
        if self.should_track(sender) and created and not raw:
            return self.add_activity_to_feed(instance)

    def activity_delete(self, sender, instance, **kwargs):
        if self.should_track(sender):
            return self.remove_activity_from_feed(instance)

    def bind_model(self, sender, **kwargs):
        if issubclass(sender, (Activity, )):
            post_save.connect(self.activity_created, sender=sender)
            post_delete.connect(self.activity_delete, sender=sender)
