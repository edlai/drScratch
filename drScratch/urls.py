from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
admin.autodiscover()

urlpatterns = (
    # Examples:
    # url(r'^$', 'drScratch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT}),
    #url(r'^profile', 'DrScratchApp.views.profileSettings',),
    url(r'^selector', 'app.views.selector',),
    url(r'^loginTournaments', 'app.views.loginTournaments',),
    url(r'^login', 'app.views.loginUser',),
    url(r'^logout', 'app.views.logoutUser',),
    url(r'^users$', 'app.views.signUpUser',),
    url(r'^statistics$', 'app.views.statistics',),
    url(r'^collaborators$', 'app.views.collaborators',),
    url(r'^reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'app.views.reset_password_confirm',name="reset_password_confirm"),
    url(r'^changePwd$', 'app.views.changePwd',),
    url(r'^organizationHash', 'app.views.organizationHash',),
    url(r'^organization$', 'app.views.signUpOrganization',),
    url(r'^organization/(\w+)', 'app.views.organization',),
    url(r'^loginOrganization$', 'app.views.loginOrganization',),
    url(r'^logoutOrganization$', 'app.views.logoutOrganization',),
    url(r'^analyzeCSV$', 'app.views.analyzeCSV',),
    #url(r'^500', 'app.views.error500',),
    #url(r'^404', 'app.views.error404',),
    url(r'learn$', 'app.views.learnUnregistered',),
    url(r'^learn/(\w+)', 'app.views.learn',),
    url(r'^createUserHash', 'app.views.createUserHash',),
    url(r'^uploadRegistered', 'app.views.uploadRegistered',),
    url(r'^myDashboard', 'app.views.myDashboard',),
    url(r'^myHistoric', 'app.views.myHistoric',),
    url(r'^myProjects', 'app.views.myProjects',),
    url(r'^myRoles', 'app.views.myRoles',),
    
    #Tournaments
    url(r'^tournaments', 'app.views.initTournaments',),
    url(r'^tourChangePwd$', 'app.views.tourChangePwd',),
    url(r'^reset_password_tournaments/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'app.views.reset_password_tournaments',name="reset_password_tournaments"),
    #Participants
    url(r'^participant/teams', 'app.views.teamsParticipant',),
    url(r'^participant/tournaments', 'app.views.tournamentsParticipant',),
    url(r'^participant/play', 'app.views.playParticipant',),
    
    #Creator
    url(r'^creator/signup', 'app.views.signUpCreator',),
    url(r'^creator/tournaments', 'app.views.tournamentsCreator',),
    url(r'^creator/challenges', 'app.views.challengesCreator',),
    url(r'^creator/admin/challenges', 'app.views.adminCreatorChallenges',),
    url(r'^creator/admin/teams', 'app.views.adminCreatorTeams',),
    url(r'^creator/admin/tournaments', 'app.views.adminCreatorTournaments',),
    url(r'^creator/admin', 'app.views.adminCreator',),
    url(r'^newChallenge', 'app.views.newChallenge',),
    url(r'^deleteChallenge', 'app.views.deleteChallenge',),
    url(r'^editChallenge', 'app.views.editChallenge',),
    url(r'^deleteTeam', 'app.views.deleteTeam',),
    url(r'^editTeamGet', 'app.views.newEditTeam',),
    url(r'^newTeamGet', 'app.views.newEditTeam',),
    url(r'^editTeamPost', 'app.views.editTeam',),
    url(r'^newTeamPost', 'app.views.newTeam',),
    url(r'^deleteTournament', 'app.views.deleteTournament',),
    url(r'^editTournamentGet', 'app.views.newEditTournament',),
    url(r'^newTournamentGet', 'app.views.newEditTournament',),
    url(r'^editTournamentPost', 'app.views.editTournament',),
    url(r'^newTournamentPost', 'app.views.newTournament',),
    url(r'^tournamentNewChallenge', 'app.views.newChallenge',),
    url(r'^tournamentNewTeam', 'app.views.newTeam',),
    url(r'^creator/newParticipants', 'app.views.creatorNewParticipants',),
    url(r'^creator/newpart/form', 'app.views.creatorNewParticipants',),
    
    url(r'^$', 'app.views.main',),
    url(r'^.*', 'app.views.redirectMain',),
    
)
