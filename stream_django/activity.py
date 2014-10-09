from django.template.defaultfilters import slugify
from django.utils.timezone import make_naive
import pytz


def model_content_type(cls):
    return '%s.%s' % (cls._meta.app_label, cls._meta.object_name)


def create_model_reference(model_instance):
    '''
    creates a reference to a model instance that can be stored in activities

    >>> from core.models import Like
    >>> like = Like.object.get(id=1)
    >>> create_model_reference(like)
    core.Like:1

    '''
    content_type = model_content_type(model_instance.__class__)
    content_id = model_instance.pk
    return '%s:%s' % (content_type, content_id)


class Activity(object):
    
    @property
    def author_feed(self):
        pass

    @classmethod
    def related_models(cls):
        '''
        Use this hook to setup related data to preload
        when reading activities from feeds.
        It must return None or a list of relationships see Django select_related for reference
        '''
        pass

    @property
    def extra_activity_data(self):
        '''
        Use this hook to setup extra activity data
        '''
        pass

    @property
    def actor_attr(self):
        '''
        Returns the model instance field that references the activity actor
        '''
        return self.user

    @property
    def actor_id(self):
        return self.actor_attr.pk

    @property
    def actor(self):
        return create_model_reference(self.actor_attr)

    @property
    def verb(self):
        model_name = slugify(self.__class__.__name__)
        return model_name
    
    @property
    def object(self):
        return create_model_reference(self)

    @property
    def foreign_id(self):
        return self.object

    @property
    def time(self):
        return make_naive(self.created_at, pytz.utc)
    
    @property
    def notify(self):
        pass
    
    def create_activity(self):
        extra_data = self.extra_activity_data
        if not extra_data:
            extra_data = {}
        
        to = self.notify
        if to:
            extra_data['to'] = to
        
        activity = dict(
            actor=self.actor,
            verb=self.verb,
            object=self.object,
            foreign_id=self.foreign_id,
            time=self.time,
            **extra_data
        )
        return activity

    @property
    def template(self):
        return "activity/%s.html" % self.verb
