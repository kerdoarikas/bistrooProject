from django import template

register = template.Library()

@register.simple_tag
def setval(val=None):
    return val
