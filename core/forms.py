# -*- coding: utf 8 -*-
from django import forms
from django.contrib.auth.models import User
from .models import Fixies, ComentFixies, Profile, Post, ComentPost

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
		fields = ('imagem_perfil', 'bio', 'git')

class PostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ('titulo', 'post','anexo', 'exibir_perfil',)

class ComentPostForm(forms.ModelForm):

	class Meta:
		model = ComentPost
		fields = ('coment',)

