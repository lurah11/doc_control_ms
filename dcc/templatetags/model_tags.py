from django import template

register = template.Library()

@register.simple_tag
def get_field_value(obj, field_name):
    return getattr(obj, field_name, None)