# -*- coding: utf 8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Permission, User

class Profile(models.Model):
	user = models.OneToOneField(User, related_name='profile')
	bio = models.TextField(verbose_name='Bio', blank=True)
	git = models.CharField(max_length=100, verbose_name='Github', blank=True)
	data_cadastro = models.DateTimeField(default=timezone.now)

class Fixies(models.Model):
	user = models.ForeignKey(User, default=1)
	titulo = models.CharField(max_length=100)
	descricao = models.TextField()
	data = models.DateTimeField(default=timezone.now)
	resolvido = models.BooleanField(default=False)
	tem_melhor_resposta = models.BooleanField(default=False)
	notificacao = models.IntegerField(default=0)

	def __str__(self):
		return self.titulo

class ComentFixies(models.Model):
	user = models.ForeignKey(User, default=1)
	fixie = models.ForeignKey(Fixies)
	coment = models.TextField()
	data = models.DateTimeField(default=timezone.now)
	melhor_resposta = models.BooleanField(default=False)

	def __str__(self):
		return '~' + self.coment + '~ em ~' + self.fixie.titulo + '~'

class Participations(models.Model):
	user = models.ForeignKey(User)
	fixie = models.ForeignKey(Fixies)
	notificacao = models.IntegerField(default=0)
	ativa_notificacao = models.BooleanField(default=True)

	def __str__(self):
		return self.user.username + ' participa de: ' + self.fixie.titulo

class Favorites(models.Model):
	user = models.ForeignKey(User)
	fixie = models.ForeignKey(Fixies)
	notificacao = models.IntegerField(default=0)

	def __str__(self):
		return self.user.username + ' favoritou: ' + self.fixie.titulo

class Followers(models.Model):
	user = models.ForeignKey(User, related_name='+')
	following = models.ForeignKey(User)
	block = models.BooleanField(default=False)
	data = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.user.username + ' esta seguindo ' + self.following.username