from django.db import models
from django.conf import settings
from stream_django.activity import Activity


class Pin(models.Model, Activity):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def activity_object_attr(self):
        return self

    @property
    def activity_actor_attr(self):
        return self.author
