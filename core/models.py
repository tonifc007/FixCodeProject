from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Permission, User

class Fixies(models.Model):
	user = models.ForeignKey(User, default=1)
	titulo = models.CharField(max_length=100)
	descricao = models.TextField()
	data = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.titulo

