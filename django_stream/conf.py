from django.conf import settings


API_KEY = getattr(settings, 'STREAM_API_KEY', None)
API_SECRET = getattr(settings, 'STREAM_API_SECRET', None)

PERSONAL_FEED = getattr(settings, 'STREAM_PERSONAL_FEED', 'user')
NOTIFICATION_FEED = getattr(settings, 'STREAM_PERSONAL_FEED', 'notification')
USER_FEEDS = getattr(settings, 'STREAM_USER_FEEDS',
    dict(flat='flat', aggregated='aggregated')
)
