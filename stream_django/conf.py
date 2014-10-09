from django.conf import settings


API_KEY = getattr(settings, 'STREAM_API_KEY', None)
API_SECRET = getattr(settings, 'STREAM_API_SECRET', None)

FEED_MANAGER_CLASS = getattr(settings, 'STREAM_FEED_MANAGER_CLASS',
    'stream_django.managers.FeedManager'
)

PERSONAL_FEED = getattr(settings, 'STREAM_PERSONAL_FEED', 'user')
NOTIFICATION_FEED = getattr(settings, 'STREAM_PERSONAL_FEED', 'notification')
USER_FEEDS = getattr(settings, 'STREAM_USER_FEEDS',
    dict(flat='flat', aggregated='aggregated')
)

DISABLE_MODEL_TRACKING = getattr(settings, 'STREAM_DISABLE_MODEL_TRACKING', False)
