from django.template import Context
from django.template import Template
from django.template import TemplateDoesNotExist
from django.test import TestCase
from stream_django.enrich import EnrichedActivity
from stream_django.exceptions import MissingDataException


simple_template = """
{%% load activity_tags %%}
{%% for activity in activities %%}
{%% render_activity activity template_prefix='%s' missing_data_policy='%s' %%}
{%% endfor %%}
"""


class TemplateTagTest(TestCase):

    def create_template(self, template_prefix='', missing_data_policy='warn'):
        return Template(simple_template % (template_prefix, missing_data_policy))

    def test_empty(self):
        ctx = Context({'activities': []})
        output = self.create_template().render(ctx)
        self.assertEqual(output.strip(), '')

    def test_default_behaviour_missing(self):
        broken_activity = EnrichedActivity({'id': '123'})
        broken_activity.track_not_enriched_field('missing', 'value')
        ctx = Context({'activities': [broken_activity]})
        output = self.create_template().render(ctx)
        self.assertEqual(output.strip(), '')

    def test_warn_missing(self):
        broken_activity = EnrichedActivity({'id': '123'})
        broken_activity.track_not_enriched_field('missing', 'value')
        ctx = Context({'activities': [broken_activity]})
        output = self.create_template(missing_data_policy='warn').render(ctx)
        self.assertEqual(output.strip(), '')

    def test_fail_missing(self):
        broken_activity = EnrichedActivity({'id': '123'})
        broken_activity.track_not_enriched_field('missing', 'value')
        ctx = Context({'activities': [broken_activity]})
        with self.assertRaises(MissingDataException):
            self.create_template(missing_data_policy='fail').render(ctx)

    def test_ignore_missing(self):
        broken_activity = EnrichedActivity({'id': '123'})
        broken_activity.track_not_enriched_field('missing', 'value')
        ctx = Context({'activities': [broken_activity]})
        output = self.create_template(missing_data_policy='ignore').render(ctx)
        self.assertEqual(output.strip(), '')

    def test_render_template_failure(self):
        activity = EnrichedActivity({'verb': 'thisone'})
        ctx = Context({'activities': [activity]})
        with self.assertRaisesMessage(TemplateDoesNotExist, 'activity/thisone.html'):
            self.create_template().render(ctx)

    def test_render_template_prefix(self):
        activity = EnrichedActivity({'verb': 'thisone'})
        ctx = Context({'activities': [activity]})

        with self.assertRaisesMessage(TemplateDoesNotExist, 'activity/prependto_thisone.html'):
            self.create_template('prependto').render(ctx)

    def test_render_template(self):
        activity = EnrichedActivity({'verb': 'tweet'})
        ctx = Context({'activities': [activity]})
        self.create_template().render(ctx)
