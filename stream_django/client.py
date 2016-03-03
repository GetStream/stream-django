from stream_django import conf
import os
import stream
from stream_django.conf import DJANGO_MAJOR_VERSION
from django.core.exceptions import ImproperlyConfigured

def init_client(raise_config_error=False):
  if conf.API_KEY and conf.API_SECRET:
      return stream.connect(conf.API_KEY, conf.API_SECRET, location=conf.LOCATION, timeout=conf.TIMEOUT)
  elif os.environ.get('STREAM_URL') is not None:
      return stream.connect()
  elif raise_config_error:
      raise ImproperlyConfigured('Stream credentials are not set in your settings')

stream_client = init_client(raise_config_error=DJANGO_MAJOR_VERSION<1.7)

