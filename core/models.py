# -*- coding: utf 8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Permission, User

class Fixies(models.Model):
	user = models.ForeignKey(User, default=1)
	titulo = models.CharField(max_length=100)
	descricao = models.TextField()
	data = models.DateTimeField(default=timezone.now)
	resolvido = models.BooleanField(default=False)
	tem_melhor_resposta = models.BooleanField(default=False)

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