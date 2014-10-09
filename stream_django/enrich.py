from collections import defaultdict
from django.db.models.loading import get_model
import operator


def combine_dicts(a, b, op=operator.add):
    return dict(a.items() + b.items() +
        [(k, op(a[k], b[k])) for k in set(b) & set(a)])


DEFAULT_FIELDS = ('actor', 'object')


class Enrich(object):

    def __init__(self, fields=DEFAULT_FIELDS):
        self.fields = fields

    def enrich_aggregated_activities(self, activities):
        references = {}
        for activity in activities:
            references = combine_dicts(references, self._collect_references(activity['activities'], self.fields))
        objects = self._fetch_objects(references)
        for activity in activities:
            self._inject_objects(activity['activities'], objects, self.fields)
        return activities

    def enrich_activities(self, activities):
        references = self._collect_references(activities, self.fields)
        objects = self._fetch_objects(references)
        self._inject_objects(activities, objects, self.fields)
        return activities

    def _collect_references(self, activities, fields):
        model_references = defaultdict(list)
        for activity in activities:
            for field in fields:
                if field in activity:
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
        if hasattr(modelClass, 'related_models') and modelClass.related_models() is not None:
            qs = qs.select_related(*modelClass.related_models())
        return qs.in_bulk(pks)

    def _fetch_objects(self, references):
        objects = defaultdict(list)
        for content_type, ids in references.items():
            model = get_model(*content_type.split('.'))
            instances = self.fetch_model_instances(model, set(ids))
            objects[content_type] = instances
        return objects

    def _inject_objects(self, activities, objects, fields):
        for activity in activities:
            for field in fields:
                if field in activity:
                    f_ct, f_id = activity[field].split(':')
                    activity[field] = objects[f_ct][int(f_id)]
