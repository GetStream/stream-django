from django.db.models.signals import pre_migrate
from django.db.models.signals import class_prepared
from stream_django.conf import FEED_MANAGER_CLASS
from stream_django.utils import get_class_from_string


feed_manager_class = get_class_from_string(FEED_MANAGER_CLASS)
feed_manager = feed_manager_class()

class_prepared = class_prepared.connect(feed_manager.bind_model)


def disable_model_tracking(sender, **kwargs):
    feed_manager.disable_model_tracking()

# disable tracking when running migrations
pre_migrate.connect(disable_model_tracking)
