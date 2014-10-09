from django.db.models.signals import class_prepared
from stream_django.conf import FEED_MANAGER_CLASS
from stream_django.conf import DISABLE_MODEL_TRACKING
from stream_django.utils import get_class_from_string


feed_manager_class = get_class_from_string(FEED_MANAGER_CLASS)
feed_manager = feed_manager_class()

if not DISABLE_MODEL_TRACKING:
    class_prepared = class_prepared.connect(feed_manager.bind_model)
