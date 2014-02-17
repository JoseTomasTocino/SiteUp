from django import template

register = template.Library()

@register.filter
def classname(obj):
    """Returns the class name of the object. To be used in a template as a filter like this:

    {{ obj | classname }}

    From http://stackoverflow.com/a/9855176/276451"""
    return obj.__class__.__name__