from django import template

register = template.Library()

@register.filter
def truncate_chars(value, max_length):
    """
    Truncate a string after a certain number of characters.
    """
    if not isinstance(value, str):
        return value
    if len(value) > max_length:
        return value[:max_length] + '...'
    return value