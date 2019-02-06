from django import template
from app.models import Game
register = template.Library()

@register.filter
def getgame_template (chTour,team):
    try:
        return Game.objects.get(challengeOfTournament=chTour, team=team)
    except Game.DoesNotExist:
        return None