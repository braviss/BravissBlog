from __future__ import unicode_literals
from django import template
from django.db.models import Model
from django.template.defaultfilters import urlencode
from django.utils.safestring import mark_safe

register = template.Library()
TELEGRAM_ENDPOINT = 'https://t.me/share/url?text=%s&url=%s'

def compile_text(context, text):
    ctx = template.context.Context(context)
    return template.Template(text).render(ctx)


def _build_url(request, obj_or_url):
    if obj_or_url is not None:
        if isinstance(obj_or_url, Model):
            return request.build_absolute_uri(obj_or_url.get_absolute_url())
        else:
            return request.build_absolute_uri(obj_or_url)
    return ''


@register.simple_tag(takes_context=True)
def post_to_telegram_url(context, title, obj_or_url):
    request = context['request']
    title = compile_text(context, title)
    url = _build_url(request, obj_or_url)
    context['telegram_url'] = mark_safe(TELEGRAM_ENDPOINT % (urlencode(title), urlencode(url)))
    return context


@register.inclusion_tag('post_to_telegram.html', takes_context=True)
def post_to_telegram(context, title, obj_or_url=None, link_text=''):
    context = post_to_telegram_url(context, title, obj_or_url)
    context['link_text'] = link_text
    return context
