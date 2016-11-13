from django import template
from ..models import ComentFixies, Fixies, Profile
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

register = template.Library()

@register.filter(name='quant_coment')
def quant_coment(value):
	return ComentFixies.objects.filter(fixie=value).count()

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