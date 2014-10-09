from collections import defaultdict
from django.db.models.loading import get_model
import operator


def combine_dicts(a, b, op=operator.add):
    return dict(a.items() + b.items() +
        [(k, op(a[k], b[k])) for k in set(b) & set(a)])


DEFAULT_FIELDS = ('actor', 'object')


class Enrich(object):

    def __init__(self, fields=None):
        if fields is None:
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

    def _fetch_objects(self, references):
        objects = defaultdict(list)
        for content_type, ids in references.items():
            model = get_model(*content_type.split('.'))
            qs = model.objects
            if hasattr(model, 'related_models') and model.related_models() is not None:
                qs = qs.select_related(*model.related_models())
            objects[content_type] = qs.in_bulk(set(ids))
        return objects

    def _inject_objects(self, activities, objects, fields):
        for activity in activities:
            for field in fields:
                if field in activity:
                    f_ct, f_id = activity[field].split(':')
                    activity[field] = objects[f_ct][int(f_id)]
