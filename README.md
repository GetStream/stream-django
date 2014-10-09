
###Stream Django

This package helps you create activity streams & newsfeeds with Django and GetStream.io.

You can check out our example app built using this library on [https://exampledjango.getstream.io](https://exampledjango.getstream.io) the code of the example app is available on Github [https://github.com/GetStream/Stream-Example-Py](https://github.com/GetStream/Stream-Example-Py)

###What can you build?

![What you can build](https://dvqg2dogggmn6.cloudfront.net/images/mood-home.png "Examples of what you can build")   


* Activity streams such as seen on Github
* A twitter style newsfeed
* A feed like instagram/ pinterest
* Facebook style newsfeeds
* A notification system


###Installation

Install stream_django package with pip:

```pip install stream_django```

add stream_django to your ```INSTALLED_APPS```

```
INSTALLED_APPS = [
    ...
    'stream_django'
]
```

Login to getstream.io and add
```STREAM_API_KEY``` and ```STREAM_API_SECRET``` to your Django settings module (you can find them in the dashboard).

###Model integration

You can have stream_django take care automatically of adding/removing model instances to user feeds; to do that let the model classes that need to be stored in feeds inherit from ```stream_django.activity.Activity```

```
class Tweet(models.Model, Activity):
    ...
```

From now on every time a Tweet is created; an activity referencing it will be added to its user' feed; feeds that follow that user will also automatically get the new tweet automatically in their feeds.

####Activity fields

Models are stored in feeds as activities; an activity is composed by the following fields: **actor**, **verb**, **object** and by other optional extra fields.  
The Activity class comes with a built-in capability of present an instance as an activity.

**object** is a reference to the model instance  
**actor** is a reference to the user attribute of the instance  
**verb** is a nice string representation of the class name

While you probably won't never need to change the object field; you might need to adjust the other two fields to fit your data.

```
class Tweet(models.Model, Activity):
    author = models.ForeignKey('core.User')

    @property
    def verb(self):
        return 'shout'

    @property
    def actor_attr(self):
        return self.author

```

####Activity extra data

Most of the times you will need to store more data than just actor,verb,object fields; to do that you need to implement the extra_activity_data method in your Activity model.
NOTE: you should only return data that json.dumps can handle (datetime instances are supported too).

```
class Tweet(models.Model, Activity):

    @property
    def extra_activity_data(self):
        return {'is_retweet': self.is_retweet }

```


###Feed manager

Django_stream comes with a feed_manager class that helps with all common feed's operations.  

####Feeds bundled with feed_manager

To get you started quickly the manager has already 3 feeds configured, this feeds are divided in two categories.

#####Personal feed:
this is where user activities are stored; something like Facebook personal timeline. You can get an instance of this feed from the manager  
```
feed_manager.get_personal_feed(user_id)
```  
#####User feeds:
this is where activity coming from followed feeds is stored; (eg. Facebook newsfeed)
```
flat_feed = feed_manager.get_user_feeds(user_id)['flat'] 
aggregated_feed = feed_manager.get_user_feeds(user_id)['aggregated'] 

```
#####Notification feed:
this is where activity that mention a user lands (eg. a comment containing @thierry should be delievered to his notification feed)
```
notification_feed = feed_manager.get_notification_feed(user_id)

```

When an Activity model is saved, the manager will send the activity to the notification feeds for the user_ids returned by the notify property:

```
class Tweet(models.Model, Activity):

    @property
    def notify(self):
        if self.is_retweet and self.parent_tweet.author != self.author:
            return [self.parent_tweet.author_id]

```



####Follow a feed
The manager comes with APIs to let a user's feeds follow another user's personal feed. This code let current user's flat and aggregated feeds follow target_user's personal feed.

```
feed_manager.follow_user(request.user.id, target_user)

```

####Low level APIs access
You can always perform operations to Stream APIs by accessing the client instance directly.

```
from stream_django.client import stream_client

special_feed = stream_client.feed('special:42')
special_feed.follow('flat:60')

```

####Activity enrichment

When you read data from feeds, a like instance will looke more or less this way:

```
{'actor': 'core.User:1', 'verb': 'like', 'object': 'core.Like:42'}
```

This is far from being ready to get in your templates; you will need to replace object and actor fields with the right models instances; to do this you can use the enrich module.

```
from stream_django.enrich import Enrich


enricher = Enrich()
feed = feed_manager.get_feed('flat', request.user.id)
activities = feed.get(limit=25)['results']
enriched_activities = feed_manager.enrich_activities(activities)
``` 

####Custom enrichment

The built-in enrichment class should cover most of your needs, there are cases though when you need more complex enrichment logic; we will cover the most common use cases here.

#####Enrich extra fields

If you store references to model instances in the activity extra_data you can use the Enrich class to take care of it for you


```
from stream_django.activity import create_model_reference


class Tweet(models.Model, Activity):

    @property
    def extra_activity_data(self):
        ref = create_model_reference(self.parent_tweet)
        return {'parent_tweet': self.parent_tweet }


# instruct the enricher to enrich actor, object and parent_tweet fields
enricher = Enrich(fields=['actor', 'object', 'parent_tweet'])
feed = feed_manager.get_feed('flat', request.user.id)
activities = feed.get(limit=25)['results']
enriched_activities = feed_manager.enrich_activities(activities)

```

#####Change how models are retrieved

The enrich class that comes with the packages tries to minimise the amount of database queries; models are grouped by their model class and then retrieved with a pk__in query. You can implement a different approach to retrieve the instances of a model subclassing the ```stream_django.enrich.Enrich``` class.

To change the retrival for every model you should override the ```fetch_model_instances``` method; in alternative you can change how certain models' are retrieved by implementing the hook function ```fetch_<model_name>_instances```


```

class MyEnrich(Enrich):
    '''
    Overwrites how model instances are fetched from the database
    '''

    def fetch_model_instances(self, modelClass, pks):
        '''
        returns a dict {id:modelInstance} with instances of model modelClass
        and pk in pks
        '''
        ...


class AnotherEnrich(Enrich):
    '''
    Overwrites how Likes instances are fetched from the database
    '''

    def fetch_like_instances(self, pks):
        return {l.id: l for l in Like.objects.cached_likes(ids)}

```


#####Prefetch related data

Sooner or later you will end up loop over the activities fetched from a feed; if you access activity's related objects (eg. activity['object'].user) on every loop you will end up firing lot of queries and get into trouble. This is something that you can easily fix by instructing the manager to preload related objects. Underneath the manager will use Django's ORM select_related (https://docs.djangoproject.com/en/dev/ref/models/querysets/#select-related).


```
class Tweet(models.Model, Activity):

    @classmethod
    def related_models(cls):
        return ['user']

```

###Templating

You can render activities using the include template tag ``` {% render_activity activity %} ```

```
{% load stream_django %}

{% for activity in activities %}
    {% render_activity activity %}
{% endfor %}

```

render_activity template tag will render the template activity/[aggregated]/%(verb)s.html with the activity as context

for example activity/tweet.html will be used to render an normal activity with verb tweet

```
{{ activity.actor.username }} said "{{ activity.object.body }} {{ activity.created_at|timesince }} ago"
```

and activity/aggregated/like.html for an aggregated activity with verb like

```
{{ activity.actor_count }} user{{ activity.actor_count|pluralize }} liked {% render_activity activity.activities.0 %}
```

If you need to support different kind of templates for the same activity, you case send a third parameter (template_prefix) to change the template selection.  

eg. this will use the template activity/[aggregated]/homepage_%(verb)s.html
```
{% render_activity activity 'homepage_' %}
```


###Settings

STREAM_API_KEY  
STREAM_API_SECRET  
STREAM_FEED_MANAGER_CLASS  
STREAM_PERSONAL_FEED  
STREAM_PERSONAL_FEED  
STREAM_USER_FEEDS  
STREAM_DISABLE_MODEL_TRACKING
