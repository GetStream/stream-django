import django
from stream_django.feed_manager import feed_manager  # noqa

version_list = [int(i) for i in django.__version__.split('.')]
major, minor = version_list[0], version_list[1]

if major < 3 or (major == 3 and minor < 2):
    # deprecated as of Django 3.2
    default_app_config = 'stream_django.apps.StreamDjangoConfig'
