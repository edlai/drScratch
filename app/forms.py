from django.forms import ModelForm
from django import forms
from models import OrganizationHash
from django.utils.translation import ugettext_lazy as _

class UploadFileForm(forms.Form):
    filename = forms.CharField(max_length=50)

class UserForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)

class NewUserForm(forms.Form):
    nickname = forms.CharField(max_length=50)
    emailUser = forms.CharField(max_length=50)
    passUser = forms.CharField(max_length=50)



class UrlForm(forms.Form):
    urlProject = forms.CharField(max_length=80)

class UpdateForm(forms.Form):
    newPass = forms.CharField(max_length=50, required=True)
    newEmail = forms.CharField (max_length=50, required=True)
#    choiceAvatar = forms.ChoiceField(choices=AVATAR_CHOICES, widget=forms.RadioSelect()

class TeacherForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)  
    hashkey = forms.CharField(max_length=50)
    #classroom = forms.CharField(max_length=50)


class OrganizationForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50) 
    password = forms.CharField(max_length=50) 
    hashkey = forms.CharField(max_length=70)  

class OrganizationHashForm(ModelForm):
    class Meta:
        model = OrganizationHash
        fields = ['hashkey']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50) 
    password = forms.CharField(max_length=50) 
    
class CreatorForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50) 
    password = forms.CharField(max_length=50) 
    hashkey = forms.CharField(max_length=70)
    
class TournamentForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': _('Tournament Name'), 'class': 'form-control input-box placeholder', 'required': 'required'}), required=True)
    description = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'placeholder': _('Tournament Description'), 'class': 'form-control input-box placeholder', 'required': 'required'}), required=True)
    
class TeamForm (forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': _('Team Name'), 'class': 'form-control input-box placeholder', 'required': 'required'}), required=True)
    description = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'placeholder': _('Team Description'), 'class': 'form-control input-box placeholder', 'required': 'required'}), required=True)
    
class EditTournamentForm(forms.Form):
    idTorneo = forms.CharField(max_length=50)
    tourName = forms.CharField(max_length=50, required=False)
    tourDesc = forms.CharField(max_length=50, required=False)
    teamName = forms.MultipleChoiceField
    teamDesc = forms.MultipleChoiceField
    
class ParticipantForm (forms.Form):
    tourName = forms.CharField(max_length=50) 
    participantName = forms.MultipleChoiceField
    
DIFFICULTY_CHOICES= [
    (0, _('None: 0')),
    (1, _('Easy: 1')),
    (2, _('Medium: 2')),
    (3, _('Hard: 3')),
    ]
    
class ChallengeForm (forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': _('Challenge Name'), 'class': 'form-control input-box placeholder', 'required': 'required'}), required=True)
    description = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'placeholder': _('Challenge Description'), 'class': 'form-control input-box placeholder', 'required': 'required'}), required=True)
    parallelism = forms.ChoiceField(widget=forms.RadioSelect, choices=DIFFICULTY_CHOICES, initial=0)
    logic = forms.ChoiceField(widget=forms.RadioSelect, choices=DIFFICULTY_CHOICES, initial=0)
    flowControl = forms.ChoiceField(widget=forms.RadioSelect, choices=DIFFICULTY_CHOICES, initial=0)
    userInteractivity = forms.ChoiceField(widget=forms.RadioSelect, choices=DIFFICULTY_CHOICES, initial=0)
    dataRepresentation = forms.ChoiceField(widget=forms.RadioSelect, choices=DIFFICULTY_CHOICES, initial=0)
    abstraction = forms.ChoiceField(widget=forms.RadioSelect, choices=DIFFICULTY_CHOICES, initial=0)
    synchronization = forms.ChoiceField(widget=forms.RadioSelect, choices=DIFFICULTY_CHOICES, initial=0)
