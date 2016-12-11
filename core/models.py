# -*- coding: utf 8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Permission, User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
import PIL
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime


def user_directory_profileimage(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/profile/{1}'.format(instance.user.username, filename)

class Areas(models.Model):
	nome_linguagem = models.CharField(max_length=100, verbose_name='Linguagem')

	def __str__(self):
		return self.nome_linguagem


class Profile(models.Model):
	user = models.OneToOneField(User, related_name='profile')
	bio = models.TextField(verbose_name='Bio', blank=True)
	git = models.CharField(max_length=100, verbose_name='Github', blank=True)
	imagem_perfil = models.ImageField(blank=True, null=True, upload_to=user_directory_profileimage)
	data_cadastro = models.DateTimeField(default=timezone.now)
	habilidades = models.ManyToManyField(Areas)
	visto_por_ultimo = models.DateTimeField(default=timezone.now)

	def save(self):
		try:
			this = Profile.objects.get(id=self.id)
			if this.imagem_perfil != self.imagem_perfil:
				this.imagem_perfil.delete(save=False)
				#this.anexo = self.anexo
			else:
				self.imagem_perfil = this.imagem_perfil
		except: pass

		if self.habilidades.count() > 5:
			raise Http404
		super(Profile, self).save()
		try:
			if self.imagem_perfil != False:
				img = PIL.Image.open(self.imagem_perfil)
				(width, height) = img.size
				print width
				print height
				if height > width:
					divisor = height/300
					width = width/divisor
					height = 300
				elif height < width:
					divisor = width/300
					height = height/divisor
					width = 300
				else:
					width = height = 300
				img = img.resize((width, height), PIL.Image.ANTIALIAS)
				img.save(self.imagem_perfil.path)
		except: pass

	def saveInstance(self):
		super(Profile, self).save()

	def delete(self):
		try:
			this = Profile.objects.get(id=self.id)
			if this.imagem_perfil:
				this.imagem_perfil.delete(save=False)
		except: pass
		super(Profile, self).delete()

	def atualiza_visto(self, usuarioLogado):
		usuarioLogado.visto_por_ultimo = timezone.now()
		usuarioLogado.save()
		return usuarioLogado.visto_por_ultimo

	def verificaDispo(self, usuarioVisitado):
		diferenca = timezone.now() - usuarioVisitado.visto_por_ultimo
		if diferenca.total_seconds() <= 10:
			return "Online"
		return self.formataData(usuarioVisitado.visto_por_ultimo)

	def formataData(self, data):
		return self.menor_que_10(data.day) + "/" + self.menor_que_10(data.month) + "/" + str(data.year) + " às " + self.menor_que_10(data.hour) + ":" + self.menor_que_10(data.minute)

	def formataDataChat(self, data):
		return self.menor_que_10(data.day) + "/" + self.menor_que_10(data.month) + "/" + str(data.year) + " às " + self.menor_que_10(data.hour) + ":" + self.menor_que_10(data.minute) + ":" + self.menor_que_10(data.second)

	def menor_que_10(self, n):
		if n < 10:
			return "0"+ str(n)
		return str(n)

	def __str__(self):
		return self.user.username

class Fixies(models.Model):
	user = models.ForeignKey(User, default=1)
	titulo = models.CharField(max_length=100)
	descricao = RichTextUploadingField(config_name='principal')
	data = models.DateTimeField(default=timezone.now)
	resolvido = models.BooleanField(default=False)
	tem_melhor_resposta = models.BooleanField(default=False)
	notificacao = models.IntegerField(default=0)
	ativa_notificacao = models.BooleanField(default=True)
	area = models.ManyToManyField(Areas)

	def __str__(self):
		return self.titulo

	def get_todos_fixies_sem_notificacao(self, usuarioLogado):
		return Fixies.objects.filter(user=usuarioLogado)[::-1]

	def get_fixies_com_novas_respostas(self, usuarioLogado):
		fixies = Fixies.objects.filter(user=usuarioLogado)
		lista = list()
		for f in fixies:
			if f.notificacao > 0 and f.ativa_notificacao == True:
				lista.append(f)
		return lista[::-1]

class ComentFixies(models.Model):
	user = models.ForeignKey(User, default=1)
	fixie = models.ForeignKey(Fixies)
	coment = RichTextUploadingField(config_name='coment')
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

	def get_participations_sem_notificacao(self, usuarioLogado):
		return Participations.objects.filter(user=usuarioLogado)

	def get_participations_com_novas_respostas(self, usuarioLogado):
		participacao = Participations.objects.filter(user=usuarioLogado)
		lista = list()
		for p in participacao:
			if p.notificacao > 0 and p.ativa_notificacao == True:
				lista.append(p)
		return lista[::-1]

class Favorites(models.Model):
	user = models.ForeignKey(User)
	fixie = models.ForeignKey(Fixies)
	notificacao = models.IntegerField(default=0)

	def __str__(self):
		return self.user.username + ' favoritou: ' + self.fixie.titulo

	def get_favorites_sem_notificacao(self, usuarioLogado):
		return Favorites.objects.filter(user=usuarioLogado)[::-1]

	def get_favorites_com_novas_respostas(self, usuarioLogado):
		favoritos = Favorites.objects.filter(user=usuarioLogado)
		lista = list()
		for f in favoritos:
			if f.notificacao > 0:
				lista.append(f)
		return lista[::-1]

class Followers(models.Model):
	user = models.ForeignKey(User, related_name='+')
	following = models.ForeignKey(User)
	block = models.BooleanField(default=False)
	data = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.user.username + ' esta seguindo ' + self.following.username

	def get_dados_seguidor(self, usuarioLogado, usuarioVisitado):
		if usuarioVisitado != usuarioLogado:
			try:
				procurarRegistro = Followers.objects.get(user=usuarioLogado, following=usuarioVisitado)
				if procurarRegistro:
					return 1
			except ObjectDoesNotExist:
				return 2
		else:
			return 0

	def get_data_que_comecou_seguir(self, usuarioLogado, usuarioVisitado):
		if self.get_dados_seguidor(usuarioLogado, usuarioVisitado) == 1:
			procurarRegistro = Followers.objects.get(user=usuarioLogado, following=usuarioVisitado)
			return procurarRegistro.data
		return None

	def relacao_de_seguindo_decrescente(self, usuario):
		#buscar seguindo pra por na página
		relacao = Followers.objects.filter(user=usuario)
		followings = []

		for pessoa in relacao:
			followings.append(pessoa.following)

		#invertendo para os ultmos serem os primeiros
		return followings[::-1]

	def relacao_de_seguidores_decrescente(self, usuario):
		#buscar seguindo pra por na página
		relacao = Followers.objects.filter(following=usuario)
		followers = []

		for pessoa in relacao:
			followers.append(pessoa.user)

		#invertendo para os ultmos serem os primeiros
		return followers[::-1]

	def get_dados_seguidor_Logado(self, usuarioVisitado):
		print "entrou"
		print("o user logado é {}".format(request.user))
		if usuarioVisitado != request.user:
			try:
				procurarRegistro = Followers.objects.get(user=request.user, following=usuarioVisitado)
				if procurarRegistro:
					return 1
			except ObjectDoesNotExist:
				return 2
		else:
			return 0

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/uploads/{1}'.format(instance.user.username, filename)

class Post(models.Model):
	user = models.ForeignKey(User, default=1)
	titulo = models.CharField(max_length=100)
	post = RichTextUploadingField(config_name='post')
	data = models.DateTimeField(default=timezone.now)
	notificacao = models.IntegerField(default=0)
	ativa_notificacao = models.BooleanField(default=True)
	exibir_perfil = models.BooleanField(default=True)
	anexo = models.FileField(blank=True, upload_to=user_directory_path)
	area = models.ManyToManyField(Areas)

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

	def get_posts_notificados(self, usuarioLogado):
		lista = list()

		posts = Post.objects.filter(user=usuarioLogado)

		for post in posts:
			if post.notificacao > 0 and post.ativa_notificacao == True:
				lista.append(post)
		return lista[::-1]

	def __str__(self):
		return self.titulo

class ComentPost(models.Model):
	user = models.ForeignKey(User, default=1)
	post = models.ForeignKey(Post)
	coment = models.TextField(verbose_name='Comentário')
	data = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return '~' + self.coment + '~ em ~' + self.post.titulo + '~'

class Message(models.Model):
	emissor = models.ForeignKey(User, related_name='+')
	receptor = models.ForeignKey(User)
	data = models.DateTimeField(default=timezone.now)
	texto = models.TextField(verbose_name='Mensagem')
	visualisada = models.BooleanField(default=False)

	def __str__(self):
		return 'Mensagem de ' + self.emissor.first_name +' para '+self.receptor.first_name

	def get_all_messages(self, usuarioLogado, usuarioVisitado):
		ms = list()
		instanciaParaRecuperarData = Profile()

		mlog = Message.objects.filter(emissor=usuarioLogado, receptor=usuarioVisitado)
		mvis = Message.objects.filter(emissor=usuarioVisitado, receptor=usuarioLogado)

		for m in mlog:ms.append(m)
		for m in mvis:
			if m.visualisada == False:
				m.visualisada = True
				m.save()
			ms.append(m)

		lista =  sorted(ms, key=lambda inst: inst.data)

		json = []

		for msg in lista:
			if msg.emissor == usuarioLogado:
				a = [0, msg.texto, instanciaParaRecuperarData.formataDataChat(msg.data)]
			else:
				a = [1, msg.texto, instanciaParaRecuperarData.formataDataChat(msg.data)]
			json.append(a)
		return json

	def get_20_messages(self, usuarioLogado, usuarioVisitado):
		ms = list()

		mlog = Message.objects.filter(emissor=usuarioLogado, receptor=usuarioVisitado)
		mvis = Message.objects.filter(emissor=usuarioVisitado, receptor=usuarioLogado)

		for m in mlog:ms.append(m)
		for m in mvis:
			if m.visualisada == False:
				m.visualisada = True
				m.save()
			ms.append(m)

		return sorted(ms, key=lambda inst: inst.data)[::-1][0:30][::-1]

	def get_messages_not_view(self, usuarioLogado, usuarioVisitado):
		a = list()
		mvis = Message.objects.filter(emissor=usuarioVisitado, receptor=usuarioLogado)

		for m in mvis:
			if m.visualisada == False:
				a.append(([m.texto], ["{}/{} - {}:{}:{}".format(m.data.month, m.data.day, m.data.hour, m.data.minute, m.data.second)]))
		return a

	def set_le_mensagens(self, usuarioLogado, usuarioVisitado):
		mvis = Message.objects.filter(emissor=usuarioVisitado, receptor=usuarioLogado)
		for m in mvis:
			if m.visualisada == False:
				m.visualisada = True
				m.save()
		return True

	def send_message(self, usuarioLogado, usuarioVisitado, mensagem):
		newMessage = Message()
		newMessage.texto = mensagem
		newMessage.emissor = usuarioLogado
		newMessage.receptor = usuarioVisitado
		newMessage.save()
		instanciaParaRecuperarData = Profile()
		return[newMessage.texto, instanciaParaRecuperarData.formataDataChat(newMessage.data)]

	def verifica_leitura_de_msg(self, usuarioLogado, usuarioVisitado):
		ms = list()

		mlog = Message.objects.filter(emissor=usuarioLogado, receptor=usuarioVisitado)
		mvis = Message.objects.filter(emissor=usuarioVisitado, receptor=usuarioLogado)

		for m in mlog:ms.append(m)
		for m in mvis:ms.append(m)

		ultimamsg = sorted(ms, key=lambda inst: inst.data)[-1]

		if ultimamsg.emissor == usuarioLogado and ultimamsg.visualisada == True:
			return True
		return False

