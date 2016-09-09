from django import forms
from django.contrib.auth.models import User
from .models import Fixies

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['username', 'password']

class FixiesForm(forms.ModelForm):
	
	class Meta:
		model = Fixies
		fields = ('titulo', 'descricao')