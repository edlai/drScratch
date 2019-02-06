from django import template
register = template.Library()

@register.filter
def player_template(List, i):
    return List[int(i)]