from django import template

register = template.Library()

def contains(val, what):
    if isinstance(val, basestring) and isinstance(what, basestring):
        return what in val
    else:
        return False

register.filter('contains', contains)
