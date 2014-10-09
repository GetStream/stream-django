from activity import Activity
from django.db.models.signals import post_delete, post_save
from stream_django.client import stream_client
from stream_django import conf


class FeedManager(object):

    def __init__(self):
        self.notification_feed = conf.NOTIFICATION_FEED
        self.user_feed = conf.USER_FEED
        self.news_feeds = conf.NEWS_FEEDS

    def get_user_feed(self, user_id, feed_type=None):
        if feed_type is None:
            feed_type = self.user_feed
        feed = stream_client.feed('%s:%s' % (feed_type, user_id))
        return feed

    def get_notification_feed(self, user_id):
        return stream_client.feed('%s:%s' % (self.notification_feed, user_id))

    def get_actor_feed(self, instance=None):
        if instance.author_feed is not None:
            return instance.author_feed
        else:
            return self.user_feed

    def follow_user(self, user_id, target_user_id):
        news_feeds = self.get_news_feeds(user_id)
        target_feed = self.get_user_feed(target_user_id)
        for feed in news_feeds.values():
            feed.follow(target_feed.feed_id)

    def unfollow_user(self, user_id, target_user_id):
        news_feeds = self.get_news_feeds(user_id)
        target_feed = self.get_user_feed(target_user_id)
        for feed in news_feeds.values():
            feed.unfollow(target_feed.feed_id)

    def get_feed(self, feed, user_id):
        return stream_client.feed('%s:%s' % (feed, user_id))

    def get_news_feeds(self, user_id):
        feeds = {}
        for feed in self.news_feeds:
            feeds[feed] = self.get_feed(feed, user_id)
        return feeds

    def activity_created(self, sender, instance, created, **kwargs):
        if created:
            activity = instance.create_activity()
            feed_type = self.get_actor_feed(instance)
            feed = self.get_feed(feed_type, instance.actor_id)
            result = feed.add_activity(activity)
            return result

    def activity_delete(self, sender, instance, **kwargs):
        feed_type = self.get_actor_feed(instance)
        feed = self.get_feed(feed_type, instance.actor_id)
        result = feed.remove_activity(foreign_id=instance.foreign_id)
        return result

    def bind_model(self, sender, **kwargs):
        if issubclass(sender, (Activity, )):
            post_save.connect(self.activity_created, sender=sender)
            post_delete.connect(self.activity_delete, sender=sender)
