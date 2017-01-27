from django import template
from ..models import ComentFixies, Fixies, Profile, Participations, Favorites, Post, Followers, ComentPost, Areas
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import os.path
import os
register = template.Library()

@register.filter(name='qfollowers')
def qfollowers(value):
	instanciaF = Followers()
	return len(instanciaF.relacao_de_seguidores_decrescente(value))

@register.filter(name='qfollowing')
def qfollowing(value):
	instanciaF = Followers()
	return len(instanciaF.relacao_de_seguindo_decrescente(value))

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
	bytes = float(os.path.getsize(value))
	print("Tamanho do arquivo: {}".format(bytes))
	if bytes < 1024:
		return ("%.2f bytes" % round(bytes,2))
	if bytes < 1024 * 1024:
		bytes = bytes/1024
		return ("%.1f KB" % round(bytes,2))
	if bytes < 1024 * 1024 * 1024:
		bytes = bytes / (1024 * 1024)
		return ("%.1f MB" % round(bytes,2))

@register.filter(name='extarquivo')
def extarquivo(value):
	return value.url.split('.')[-1]

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

@register.filter(name='formatDataBP')
def formatDataBP(value):
	instanciaProfile = Profile()
	return instanciaProfile.formataDataChat(value)

@register.filter(name='quant_Area')
def quant_Area_Fix(value):
	instanciaArea = Areas()
	return len(instanciaArea.busca_fix(value))+len(instanciaArea.busca_post(value))

@register.filter(name='quant_Area_Fix')
def quant_Area_Fix(value):
	instanciaArea = Areas()
	return len(instanciaArea.busca_fix(value))

@register.filter(name='quant_Area_Post')
def quant_Area_Post(value):
	instanciaArea = Areas()
	return len(instanciaArea.busca_post(value))

@register.filter(name='quant_Area_User')
def quant_Area_Post(value):
	instanciaArea = Areas()
	return len(instanciaArea.busca_user(value))

@register.filter(name='auxArea')
def auxArea(value):
	return Areas.objects.all()

@register.filter(name='quantSearchFix')
def quantSearchFix(value):
	instanciaFixies = Fixies()
	return len(instanciaFixies.search_fix(value))

@register.filter(name='quantSearchPost')
def quantSearchPost(value):
	instanciaPost = Post()
	return len(instanciaPost.search_post(value))

@register.filter(name='quantSearchUser')
def quantSearchUser(value):
	instanciaProfile = Profile()
	return len(instanciaProfile.search_user(value))

@register.filter(name='quantSearchAll')
def quantSearchAll(value):
	instanciaFixies = Fixies()
	instanciaPost = Post()
	instanciaProfile = Profile()
	return len(instanciaFixies.search_fix(value)) + len(instanciaPost.search_post(value)) + len(instanciaProfile.search_user(value))