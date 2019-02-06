from django import template
register = template.Library()

@register.filter
def getdict_template (obj, attribute):
    try:
        return obj[attribute]
    except AttributeError:
        return  ''
