from django import template
from ..models import ComentFixies, Fixies

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