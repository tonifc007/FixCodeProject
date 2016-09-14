# -*- coding: utf 8 -*-
from django import forms
from django.contrib.auth.models import User
from .models import Fixies, ComentFixies, Profile

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['username', 'password']

class UserFormRegister(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	repassword = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['first_name','last_name','username', 'password', 'repassword']

class FixiesForm(forms.ModelForm):
	
	class Meta:
		model = Fixies
		fields = ('titulo', 'descricao')

class ComentForm(forms.ModelForm):

	class Meta:
		model = ComentFixies
		fields = ('coment',)

class EditProfile(forms.ModelForm):

	class Meta:
		model = Profile
		fields = ('bio', 'git')