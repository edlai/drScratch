from django import template
from app.models import ChallengesOfTournament
register = template.Library()

@register.filter
def getchoftour_template (ch,tour):
    try:
        return ChallengesOfTournament.objects.get(challenge=ch, tournament=tour)
    except ChallengesOfTournament.DoesNotExist:
        return None