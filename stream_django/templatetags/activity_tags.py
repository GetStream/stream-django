import django
from django import template
from django.template import Context, loader
from stream_django.exceptions import MissingDataException
import logging


logger = logging.getLogger(__name__)
register = template.Library()

LOG = 'warn'
IGNORE = 'ignore'
FAIL = 'fail'

missing_data_policies = [LOG, IGNORE, FAIL]


def handle_not_enriched_data(activity, policy):
    message = 'could not enrich field(s) %r for activity #%s' % (activity.not_enriched_data, activity.get('id'))
    if policy == IGNORE:
        pass
    elif policy == FAIL:
        raise MissingDataException(message)
    elif policy == LOG:
        logger.warn(message)
    else:
        raise TypeError('%s is not a valid missing_data_policy' % policy)


def render_activity(context, activity, template_prefix='', missing_data_policy=LOG):
    if hasattr(activity, 'enriched') and not activity.enriched:
        handle_not_enriched_data(activity, missing_data_policy)
        return ''

    if template_prefix != '':
        template_prefix = '%s_' % template_prefix

    if 'activities' in activity:
        template_name = "activity/aggregated/%s%s.html" % (template_prefix, activity['verb'])
    else:
        template_name = "activity/%s%s.html" % (template_prefix, activity['verb'])

    tmpl = loader.get_template(template_name)
    context['activity'] = activity

    if django.VERSION < (1, 11):
        context = Context(context)
    elif isinstance(context, Context):
        context = context.flatten()

    return tmpl.render(context)


register.simple_tag(takes_context=True)(render_activity)
