from django import template
from ..models import ComentFixies, Fixies, Profile, Participations, Favorites, Post, Followers, ComentPost
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import os.path

register = template.Library()

@register.filter(name='quant_coment')
def quant_coment(value):
	return ComentFixies.objects.filter(fixie=value).count()

@register.filter(name='quant_comentP')
def quant_comentP(value):
	return ComentPost.objects.filter(post=value).count()

@register.filter(name='l')
def l(value):
	return value.count()

@register.filter(name='nomearquivo')
def nomearquivo(value):
	return value.url.split('/')[-1]

@register.filter(name='imagemperfil')
def imagemperfil(value):
	try:
		perfil = Profile.objects.get(user=value)
		if perfil:			
			if perfil.imagem_perfil:
				return perfil.imagem_perfil.url
			else:
				return False
	except ObjectDoesNotExist:
		return False

@register.filter(name='fixoupost')
def fixoupost(value):
	if type(value) == Fixies:
		return True
	else:
		return False

@register.filter(name='subtempo')
def subtempo(value):
	a = timezone.now() - value
	return a.days

@register.filter(name='quant_fix')
def quant_fix(value):
	f = Fixies.objects.filter(user=value)
	return f.count()

@register.filter(name='quant_part')
def quant_part(value):
	f =  Participations.objects.filter(user=value)
	return f.count()

@register.filter(name='quant_fav')
def quant_fav(value):
	f = Favorites.objects.filter(user=value)
	return f.count()

@register.filter(name='quant_post')
def quant_post(value):
	f = Post.objects.filter(user=value)
	return f.count()

@register.filter(name='dados_segue')
def dados_segue(value):
	d = Followers()
	a =  d.get_dados_seguidor_Logado(value)
	print a
	return a

@register.filter(name='quant_FSnotify')
def quant_FSnotify(value):
	f = Fixies()
	quant = f.get_todos_fixies_sem_notificacao(value)
	return len(quant)

@register.filter(name='quant_FCnotify')
def quant_FCnotify(value):
	f = Fixies()
	quant = f.get_fixies_com_novas_respostas(value)
	return len(quant)

@register.filter(name='quant_PartSnotify')
def quant_PartSnotify(value):
	f = Participations()
	quant = f.get_participations_sem_notificacao(value)
	return len(quant)

@register.filter(name='quant_PartCnotify')
def quant_PartCnotify(value):
	f = Participations()
	quant = f.get_participations_com_novas_respostas(value)
	return len(quant)

@register.filter(name='quant_FaSnotify')
def quant_FaSnotify(value):
	f = Favorites()
	quant = f.get_favorites_sem_notificacao(value)
	return len(quant)

@register.filter(name='quant_FaCnotify')
def quant_FaCnotify(value):
	f = Favorites()
	quant = f.get_favorites_com_novas_respostas(value)
	return len(quant)

@register.filter(name='quant_PSnotify')
def quant_PSnotify(value):	
	return len(Post.objects.filter(user=value))

@register.filter(name='quant_PCnotify')
def quant_PCnotify(value):
	p = Post()
	quant = p.get_posts_notificados(value)
	return len(quant)

@register.filter(name='verificaArquivo')
def verificaArquivo(value):
	return os.path.isfile(value)