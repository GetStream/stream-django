from stream_django import conf
import os
import stream
from stream_django.conf import DJANGO_MAJOR_VERSION
from django.core.exceptions import ImproperlyConfigured

def init_client(mayRaise=False):
  if conf.API_KEY and conf.API_SECRET:
      stream_client = stream.connect(
          conf.API_KEY, conf.API_SECRET, location=conf.LOCATION, timeout=conf.TIMEOUT)
  elif os.environ.get('STREAM_URL') is not None:
      stream_client = stream.connect()
  else:
      stream_client = None
      if mayRaise:
        raise ImproperlyConfigured('Stream credentials are not set in your settings')

stream_client = init_client(mayRaise=DJANGO_MAJOR_VERSION<1.7)

