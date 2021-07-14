from django.db import models
from django.template.defaultfilters import slugify
from django.utils.timezone import is_aware
from django.utils.timezone import make_naive
import pytz


def model_content_type(cls):
    return '%s.%s' % (cls._meta.app_label, cls._meta.object_name)


def create_reference(reference):
    if isinstance(reference, (models.Model, )):
        return create_model_reference(reference)
    return reference


def create_model_reference(model_instance):
    '''
    creates a reference to a model instance that can be stored in activities

    >>> from core.models import Like
    >>> like = Like.object.get(id=1)
    >>> create_reference(like)
    core.Like:1

    '''
    content_type = model_content_type(model_instance.__class__)
    content_id = model_instance.pk
    return '%s:%s' % (content_type, content_id)


class Activity(object):
    
    @property
    def activity_author_feed(self):
        '''
        The name of the feed where the activity will be stored; this is normally
        used by the manager class to determine if the activity should be stored elsewhere than
        settings.USER_FEED
        '''
        pass

    @classmethod
    def activity_related_models(cls):
        '''
        Use this hook to setup related models to load during enrichment.
        It must return None or a list of relationships see Django select_related for reference
        '''
        pass

    @property
    def extra_activity_data(self):
        '''
        Use this hook to store extra data in activities.
        If you need to store references to model instances you should use create_model_reference

        eg:
            @property
            def activity_extra_activity_data(self):
                dict('parent_user'=create_reference(self.parent_user))
        '''
        pass

    @property
    def activity_actor_attr(self):
        '''
        Returns the model instance field that references the activity actor
        '''
        return self.user

    @property
    def activity_object_attr(self):
        '''
        Returns the reference to the object of the activity
        '''
        return self

    @property
    def activity_actor_id(self):
        return self.activity_actor_attr.pk

    @property
    def activity_actor(self):
        return create_reference(self.activity_actor_attr)

    @property
    def activity_verb(self):
        model_name = slugify(self.__class__.__name__)
        return model_name
    
    @property
    def activity_object(self):
        return create_reference(self.activity_object_attr)

    @property
    def activity_foreign_id(self):
        return self.activity_object

    @property
    def activity_time(self):
        atime = self.created_at
        if is_aware(self.created_at):
            atime = make_naive(atime, pytz.utc)
        return atime
    
    @property
    def activity_notify(self):
        pass
    
    def create_activity(self):
        extra_data = self.extra_activity_data
        if not extra_data:
            extra_data = {}
        
        to = self.activity_notify
        if to:
            extra_data['to'] = [f.id for f in to]
        
        activity = dict(
            actor=self.activity_actor,
            verb=self.activity_verb,
            object=self.activity_object,
            foreign_id=self.activity_foreign_id,
            time=self.activity_time,
            **extra_data
        )
        return activity
