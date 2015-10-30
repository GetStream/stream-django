from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured
from stream_django.conf import is_valid_config

class StreamDjangoConfig(AppConfig):
    name = 'stream_django'
    verbose_name = "Stream Django"

    def ready(self):
      if not is_valid_config():
        raise ImproperlyConfigured('Stream credentials are not set in your settings')
