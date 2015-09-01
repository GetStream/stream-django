from stream_django import conf
import os
import stream
from django.core.exceptions import ImproperlyConfigured

if conf.API_KEY and conf.API_SECRET:
    stream_client = stream.connect(
        conf.API_KEY, conf.API_SECRET, location=conf.LOCATION, timeout=conf.TIMEOUT)
else:
    stream_client = stream.connect()

if os.environ.get('STREAM_URL') is None and not(conf.API_KEY and conf.API_SECRET):
    raise ImproperlyConfigured('Stream credentials are not set in your settings')
