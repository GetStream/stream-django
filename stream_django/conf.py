import django
import os
from django.conf import settings

API_KEY = getattr(settings, 'STREAM_API_KEY', None)
API_SECRET = getattr(settings, 'STREAM_API_SECRET', None)
LOCATION = getattr(settings, 'STREAM_LOCATION', None)
TIMEOUT = getattr(settings, 'STREAM_TIMEOUT', 6.0)

FEED_MANAGER_CLASS = getattr(settings, 'STREAM_FEED_MANAGER_CLASS',
    'stream_django.managers.FeedManager'
)

USER_FEED = getattr(settings, 'STREAM_USER_FEED', 'user')
NEWS_FEEDS = getattr(settings, 'STREAM_NEWS_FEEDS',
    {'timeline':'timeline', 'timeline_aggregated':'timeline_aggregated'}
)
NOTIFICATION_FEED = getattr(settings, 'STREAM_PERSONAL_FEED', 'notification')

DISABLE_MODEL_TRACKING = getattr(settings, 'STREAM_DISABLE_MODEL_TRACKING', False)

DJANGO_MAJOR_VERSION = django.VERSION[0] + (0.1*django.VERSION[1])

def is_valid_config():
  return (API_KEY and API_SECRET) or os.environ.get('STREAM_URL')
