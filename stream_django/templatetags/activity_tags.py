from django import template
from django.template import Context, loader


register = template.Library()


def render_activity(context, activity, template_prefix=''):
    if template_prefix != '':
        template_prefix = '_%s' % template_prefix
    if 'activities' in activity:
        template_name = "activity/aggregated/%s%s.html" % (template_prefix, activity['verb'])
    else:
        template_name = "activity/%s%s.html" % (template_prefix, activity['verb'])
    tmpl = loader.get_template(template_name)
    context['activity'] = activity
    context = Context(context)
    return tmpl.render(context)


register.simple_tag(takes_context=True)(render_activity)
