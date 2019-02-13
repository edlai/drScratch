from background_task import background
from app.models import Tournament, Game, ChallengesOfTournament
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.translation import ugettext as _

@background
def summary_email(tour_id, email):
    tour = Tournament.objects.get(id=tour_id)
    chTour = ChallengesOfTournament.objects.filter(tournament=tour)
    games = Game.objects.none()
    for c in chTour:
        games = games | Game.objects.filter(challengeOfTournament=c, completed=False, done=True)
    if games:
        try:
            body = render_to_string("tournaments/creator/email_resumen.html")
            subject = _("Dr. Scratch Tournaments: Manual Validation Summary")
            sender ="no-reply@drscratch.org"
            to = [email]
            email = EmailMessage(subject,body,sender,to)
            email.send()
        except Exception as e:
            print '%s (%s)' % (e.message, type(e))