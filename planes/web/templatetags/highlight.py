from re import IGNORECASE, compile, escape
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='highlight')
def highlight(text, search):
    words = [w.strip() for w in search.split(' ')]
    rgx = compile(escape(search), IGNORECASE)
    print(words)
    return mark_safe(
        rgx.sub(
            lambda m: '<b class="text-gray-500">{}</b>'.format(m.group()),
            text
        )
    )