# -*- coding: utf 8 -*-
from django import forms
from django.contrib.auth.models import User
from .models import Fixies, ComentFixies

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['username', 'password']

class FixiesForm(forms.ModelForm):
	
	class Meta:
		model = Fixies
		fields = ('titulo', 'descricao')

class ComentForm(forms.ModelForm):

	class Meta:
		model = ComentFixies
		fields = ('coment',)