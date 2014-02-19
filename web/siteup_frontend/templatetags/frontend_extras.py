import logging
logger = logging.getLogger(__name__)

from django import template

register = template.Library()

@register.filter
def classname(obj):
    """Returns the class name of the object. To be used in a template as a filter like this:

    {{ obj | classname }}

    From http://stackoverflow.com/a/9855176/276451"""
    return obj.__class__.__name__


@register.filter
def verbose_name(obj):
    """Returns the class name of a model. To be used in a template as a filter"""

    logger.info(object)
    return obj._meta.verbose_name