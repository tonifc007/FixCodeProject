from django import template
from ..models import ComentFixies, Fixies

register = template.Library()

@register.filter(name='quant_coment')
def quant_coment(value):
	return ComentFixies.objects.filter(fixie=value).count()