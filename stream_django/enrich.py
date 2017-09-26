import collections
from collections import defaultdict
import operator
import itertools

try:
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model


def combine_dicts(a, b, op=operator.add):
    return dict(list(a.items()) + list(b.items()) +
        [(k, op(a[k], b[k])) for k in set(b) & set(a)])


DEFAULT_FIELDS = ('actor', 'object')


class EnrichedActivity(collections.MutableMapping):

    def __init__(self, activity_data):
        self.activity_data = activity_data
        self.not_enriched_data = {}

    def __getitem__(self, key):
        return self.activity_data[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.activity_data[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.activity_data[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.activity_data)

    def __len__(self):
        return len(self.activity_data)

    def __keytransform__(self, key):
        return key

    def __repr__(self):
        return "EnrichedActivity(activity_data=%s, not_enriched_data=%s)" % (str(self.activity_data),
                                                                             str(self.not_enriched_data))

    def track_not_enriched_field(self, field, value):
        self.not_enriched_data[field] = value

    @property
    def enriched(self):
        return len(self.not_enriched_data.keys()) == 0


class Enrich(object):

    def __init__(self, fields=DEFAULT_FIELDS):
        self.fields = fields

    def enrich_aggregated_activities(self, activities):
        references = {}
        for activity in activities:
            activity['activities'] = self.wrap_activities(activity['activities'])
            references = combine_dicts(references, self._collect_references(activity['activities'], self.fields))
        objects = self._fetch_objects(references)
        for activity in activities:
            self._inject_objects(activity['activities'], objects, self.fields)
        return activities

    def enrich_activities(self, activities):
        activities = self.wrap_activities(activities)
        references = self._collect_references(activities, self.fields)
        objects = self._fetch_objects(references)
        self._inject_objects(activities, objects, self.fields)
        return activities

    def wrap_activities(self, activities):
        return [EnrichedActivity(a) for a in activities]

    def is_ref(self, activity, field):
        return len(activity[field].split(':')) == 2 if activity.get(field) else False

    def _collect_references(self, activities, fields):
        model_references = defaultdict(list)
        for activity, field in itertools.product(activities, fields):
            if not self.is_ref(activity, field):
                continue
            f_ct, f_id = activity[field].split(':')
            model_references[f_ct].append(f_id)
        return model_references

    def fetch_model_instances(self, modelClass, pks):
        '''
        returns a dict {id:modelInstance} with instances of model modelClass
        and pk in pks
        '''
        hook_function_name = 'fetch_%s_instances' % (modelClass._meta.object_name.lower(), )
        if hasattr(self, hook_function_name):
            return getattr(self, hook_function_name)(pks)
        qs = modelClass.objects
        if hasattr(modelClass, 'activity_related_models') and modelClass.activity_related_models() is not None:
            qs = qs.select_related(*modelClass.activity_related_models())
        return qs.in_bulk(pks)

    def _fetch_objects(self, references):
        objects = defaultdict(list)
        for content_type, ids in references.items():
            model = get_model(*content_type.split('.'))
            ids = set(ids)
            instances = self.fetch_model_instances(model, ids)
            objects[content_type] = instances
        return objects

    def _inject_objects(self, activities, objects, fields):
        for activity, field in itertools.product(activities, fields):
            if not self.is_ref(activity, field):
                continue
            f_ct, f_id = activity[field].split(':')
            model = get_model(*f_ct.split('.'))
            f_id = model._meta.pk.to_python(f_id)

            instance = objects[f_ct].get(f_id)
            if instance is None:
                activity.track_not_enriched_field(field, activity[field])
            else:
                activity[field] = self.enrich_instance(instance)

    def enrich_instance(self, instance):
        return instance
