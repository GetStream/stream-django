
###Stream_django

This package helps you create user feeds and news feeds with Django and GetStream.io.

You can check out our example app built using this library on [https://exampledjango.getstream.io](https://exampledjango.getstream.io) the code of the example app is available on Github [https://github.com/GetStream/Stream-Example-Py](https://github.com/GetStream/Stream-Example-Py)

###Features
Settings integration    
Model integration  
Feed manager  
Templating    

###Installation

Install django_stream package with pip:

```pip install django_stream```

add django_stream to your ```INSTALLED_APPS```

```
INSTALLED_APPS = [
    ...
    'django_stream'
]
```

Login to getstream.io and add
```STREAM_API_KEY``` and ```STREAM_API_SECRET``` to your Django settings module (you can find them in the dashboard).

###Model integration

You can have django_stream take care automatically of adding/removing model instances to user feeds; to do that let the model classes that need to be stored in feeds inherit from ```django_stream.activity.Activity```

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
from django_stream.client import stream_client

special_feed = stream_client.feed('special:42')
special_feed.follow('flat:60')

```

####Activity enrichment

Another useful feature of this module is that, once you read data from feeds, you don't have to fetch all the data referenced in the activities. The feed manager exposes a functions to efficiently "enrich" activities and aggregated activities.

```
feed = feed_manager.get_feed('flat', request.user.id)
activities = feed.get(limit=25)['results']
enriched_activities = feed_manager.enrich_activities(activities)
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
