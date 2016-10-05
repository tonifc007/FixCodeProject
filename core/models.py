# -*- coding: utf 8 -*-
from __future__ import unicode_literals

from django.db import models  
from django.utils import timezone
from django.contrib.auth.models import Permission, User
from ckeditor.fields import RichTextField


def user_directory_profileimage(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/profile/{1}'.format(instance.user.username, filename)

class Profile(models.Model):
	user = models.OneToOneField(User, related_name='profile')
	bio = models.TextField(verbose_name='Bio', blank=True)
	git = models.CharField(max_length=100, verbose_name='Github', blank=True)
	imagem_perfil = models.ImageField(blank=True, null=True, upload_to=user_directory_profileimage)
	data_cadastro = models.DateTimeField(default=timezone.now)

	def save(self):
		try:
			this = Profile.objects.get(id=self.id)
			if this.imagem_perfil != self.imagem_perfil:
				this.imagem_perfil.delete(save=False)
				#this.anexo = self.anexo
			else:
				self.imagem_perfil = this.imagem_perfil
		except: pass
		super(Profile, self).save()

	def delete(self):
		try:
			this = Profile.objects.get(id=self.id)
			if this.imagem_perfil:
				this.imagem_perfil.delete(save=False)
		except: pass
		super(Profile, self).delete()

class Fixies(models.Model):
	user = models.ForeignKey(User, default=1)
	titulo = models.CharField(max_length=100)
	descricao = RichTextField(config_name='principal')
	data = models.DateTimeField(default=timezone.now)
	resolvido = models.BooleanField(default=False)
	tem_melhor_resposta = models.BooleanField(default=False)
	notificacao = models.IntegerField(default=0)
	ativa_notificacao = models.BooleanField(default=True)

	def __str__(self):
		return self.titulo

class ComentFixies(models.Model):
	user = models.ForeignKey(User, default=1)
	fixie = models.ForeignKey(Fixies)
	coment = RichTextField(config_name='coment')
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

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/uploads/{1}'.format(instance.user.username, filename)

class Post(models.Model):
	user = models.ForeignKey(User, default=1)
	titulo = models.CharField(max_length=100)
	post = RichTextField(config_name='principal')
	data = models.DateTimeField(default=timezone.now)
	notificacao = models.IntegerField(default=0)
	ativa_notificacao = models.BooleanField(default=True)
	exibir_perfil = models.BooleanField(default=True)
	anexo = models.FileField(blank=True, null=True, upload_to=user_directory_path)

	def save(self):
		try:
			this = Post.objects.get(id=self.id)
			if this.anexo != self.anexo:
				this.anexo.delete(save=False)
				#this.anexo = self.anexo
			else:
				self.anexo = this.anexo
		except: pass
		super(Post, self).save()

	def delete(self):
		try:
			this = Post.objects.get(id=self.id)
			if this.anexo:
				this.anexo.delete(save=False)
		except: pass
		super(Post, self).delete()

	def __str__(self):
		return self.titulo

class ComentPost(models.Model):
	user = models.ForeignKey(User, default=1)
	post = models.ForeignKey(Post)
	coment = RichTextField(config_name='coment')
	data = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return '~' + self.coment + '~ em ~' + self.post.titulo + '~'