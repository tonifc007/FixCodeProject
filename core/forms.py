# -*- coding: utf 8 -*-
from django import forms
from django.contrib.auth.models import User
from .models import Fixies, ComentFixies, Profile, Post, ComentPost, Areas

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
	area = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Areas.objects.all())
	class Meta:
		model = Fixies
		fields = ('titulo', 'descricao', 'area')


class ComentForm(forms.ModelForm):

	class Meta:
		model = ComentFixies
		fields = ('coment',)


class EditProfile(forms.ModelForm):
	habilidades = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Areas.objects.all())
	class Meta:
		model = Profile
		fields = ('imagem_perfil', 'bio', 'git', 'habilidades',)

class PostForm(forms.ModelForm):
	area = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Areas.objects.all())
	class Meta:
		model = Post
		fields = ('titulo', 'post','anexo', 'exibir_perfil','area')

class ComentPostForm(forms.ModelForm):

	class Meta:
		model = ComentPost
		fields = ('coment',)

