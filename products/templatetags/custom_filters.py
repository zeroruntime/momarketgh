from django import template

register = template.Library()

@register.filter
def endswith(value, arg):
    """Returns True if the value ends with the argument"""
    if not isinstance(value, str):
        return False
    return value.lower().endswith(arg.lower())
