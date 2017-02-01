# -*- coding: utf 8 -*-
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Fixies, ComentFixies, Participations, Favorites, Profile, Followers, Post, ComentPost, Areas, Message, Blocked
from django.contrib.auth import authenticate, login, logout, get_user
from .forms import UserForm, FixiesForm, ComentForm, UserFormRegister, EditProfile, PostForm, ComentPostForm, FeedbackForm
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
import json
import PIL
from django.utils import timezone

FILE_TYPES = ['pdf', 'doc', 'txt', 'zip', 'rar', '7z']
FILE_TYPES_IMAGE = ['jpg', 'jpeg']

def index(request):
	if not request.user.is_authenticated():
		print("foi no if")
		return render(request, 'core/login.html')
	else:
		perfil = get_object_or_404(Profile, user=request.user)
		if perfil.ativo == False:
			return edit_details_profile(request)

		#todos os fixies e posts mostrados no index ficam guardados nesta variável
		fixies = []

		#recolhe fixies e posts das habilidades
		for f in Fixies.objects.all():
			for f1 in f.area.all():
				for p in perfil.habilidades.all():
					if f1 == p:
						print("{} - {}".format(f1, p))
						fixies.append(f)
		for p in Post.objects.all():
			for p1 in p.area.all():
				for a in perfil.habilidades.all():
					if p1 == a:
						fixies.append(p)

		#recolhe fixies e posts das pessoas que o usuário segue
		for user in Followers.objects.filter(user=request.user):
			postsdosseguidos = Post.objects.filter(user=user.following)
			fixesdosseguidos = Fixies.objects.filter(user=user.following)
			fixies.extend(list(postsdosseguidos))
			fixies.extend(list(fixesdosseguidos))


		#recolhe seus próprios fixies e posts
		myfixies = Fixies.objects.filter(user=request.user)
		myposts = Post.objects.filter(user=request.user)
		fixies.extend(list(myfixies))
		fixies.extend(list(myposts))

 		#remove todas as duplicatas e ordena por data mais recente
		fixies = sorted(list(set(fixies)), key=lambda inst: inst.data, reverse=True)

		#buscar seguindo pra por na página
		relacao = Followers.objects.filter(user=request.user)
		followings = []

		for pessoa in relacao:
			followings.append(pessoa.following)
		print "pausa"
		#invertendo para os ultmos serem os primeiros
		followings = followings[::-1]
		print "pausa"

		instanciaMessage = Message()
		#quantidade de pessoas que mandaram mensagens
		quantidade_mensagens = instanciaMessage.count_messages(request.user)


		#sistema de paginação
		paginator = Paginator(fixies, 5)
		page = request.GET.get('page')

		instanciaFollowers = Followers()

		comentariosDosSeguindo = instanciaFollowers.get_timeline_friends_activities(followings)

		try:
			relations = paginator.page(page)
			print(relations)
		except PageNotAnInteger:
			relations = paginator.page(1)
		except EmptyPage:
			relations = paginator.page(paginator.num_pages)

		return render(request, 'core/index.html', {'relations':relations, 'profile':perfil,'comentariosDosSeguindo':comentariosDosSeguindo[0:10], 'quantidade_mensagens':quantidade_mensagens, 'qposts': len(fixies)})

def sobre(request):
	if request.user.is_authenticated():
		eu = get_object_or_404(Profile, user=request.user)
	else:
		eu = None
	return render(request, 'core/sobre.html', {'eu':eu})

def notificaAll(request):
	if not request.user.is_authenticated():
		print("foi no if")
		return render(request, 'core/login.html')
	else:
		response_data = 0
		myfixies = Fixies.objects.filter(user=request.user)
		
		for fix in myfixies:
			if fix.notificacao > 0:
				response_data += 1


		myrelationships = Participations.objects.filter(user=request.user)
		for fix in myrelationships:
			if fix.notificacao > 0:
				response_data += 1

		myposts = Post.objects.filter(user=request.user)
		for post in myposts:
			if post.notificacao > 0:
				print "incrementa"
				response_data += 1

		instanciaMessage = Message()
		#quantidade de pessoas que mandaram mensagens
		response_data += instanciaMessage.count_messages(request.user)

		return HttpResponse(json.dumps(response_data), content_type="application/json")
	return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")

def quantTL(request):
	if not request.user.is_authenticated():
		print("foi no if")
		return render(request, 'core/login.html')
	else:
		perfil = get_object_or_404(Profile, user=request.user)

		#todos os fixies e posts mostrados no index ficam guardados nesta variável
		fixies = []

		#recolhe fixies e posts das habilidades
		for f in Fixies.objects.all():
			for f1 in f.area.all():
				for p in perfil.habilidades.all():
					if f1 == p:
						print("{} - {}".format(f1, p))
						fixies.append(f)
		for p in Post.objects.all():
			for p1 in p.area.all():
				for a in perfil.habilidades.all():
					if p1 == a:
						fixies.append(p)

		#recolhe fixies e posts das pessoas que o usuário segue
		for user in Followers.objects.filter(user=request.user):
			postsdosseguidos = Post.objects.filter(user=user.following)
			fixesdosseguidos = Fixies.objects.filter(user=user.following)
			fixies.extend(list(postsdosseguidos))
			fixies.extend(list(fixesdosseguidos))


		#recolhe seus próprios fixies e posts
		myfixies = Fixies.objects.filter(user=request.user)
		myposts = Post.objects.filter(user=request.user)
		fixies.extend(list(myfixies))
		fixies.extend(list(myposts))

		response_data = len(set(fixies))

		return HttpResponse(json.dumps(response_data), content_type="application/json")
	return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")

def notificaIndex(request):
	if not request.user.is_authenticated():
		print("foi no if")
		return render(request, 'core/login.html')
	else:
		myfixies = Fixies.objects.filter(user=request.user)
		response_data = 0
		for fix in myfixies:
			if int(fix.notificacao) > 0:
				response_data += 1
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")

def notificaIndexParticipation(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		myrelationships = Participations.objects.filter(user=request.user)
		response_data = 0
		for fix in myrelationships:
			if int(fix.notificacao) > 0:
				response_data += 1
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")

def notificaIndexPosts(request):
	if not request.user.is_authenticated():
		print("foi no if")
		return render(request, 'core/login.html')
	else:
		myposts = Post.objects.filter(user=request.user)
		response_data = 0
		for post in myposts:
			if int(post.notificacao) > 0:
				print "incrementa"
				response_data += 1
		print response_data
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")


def register(request):
	if not request.user.is_authenticated():
		form = UserFormRegister(request.POST or None)
		if form.is_valid():
			user = form.save(commit=False)
			name = form.cleaned_data['first_name']
			lastname = form.cleaned_data['last_name']
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			repassword = form.cleaned_data['repassword']
			if password != repassword:
				if name == '' or lastname == '':
					return render(request, 'core/register.html', {'form':form, 'error_de_reg': 'Senhas não conferem', 'error_name':'* Este campo é obrigatório.'})
				else:
					return render(request, 'core/register.html', {'form':form, 'error_de_reg': 'Senhas não conferem'})
			elif name == '' or lastname == '':
				return render(request, 'core/register.html', {'form':form, 'error_name':'* Este campo é obrigatório.'})
			user.set_password(password)
			user.save()

			print("usuário: {} - senha: {}".format(username, password))

			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					newprofile = Profile()
					newprofile.user = request.user
					newprofile.saveInstance()
					return redirect('/editprofile/')
		return render(request, 'core/register.html', {'form':form})
	else:
		raise Http404

def settings(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		detalhes = get_object_or_404(Profile, user=request.user)
		#form = UserFormRegister(request.POST or None, instance=request.user)
		if request.POST:
			print 'entrou na funçao'

			name = request.POST.get('first_name')
			lastname = request.POST.get('last_name')
			#username = request.POST.get('username')
			password = request.POST.get('password')
			repassword = request.POST.get('repassword')
			oldpassword = request.POST.get('oldpassword')
			print name
			print lastname
			print password
			print repassword
			print oldpassword

			if name == '' or lastname == '' or password == '' or repassword == '' or oldpassword == '':
				return render(request, 'core/settings.html', {'error_name':'* Este campo é obrigatório.', 'profile':detalhes})

			if request.user.check_password(oldpassword) == False:
				print 'senha incorreta'
				return render(request, 'core/settings.html', {'error_de_senha': 'Senha atual está incorreta', 'profile':detalhes})

			if password != repassword:
				return render(request, 'core/settings.html', {'error_de_reg': 'Senhas não conferem'})

			request.user.first_name = name
			request.user.last_name = lastname
			request.user.set_password(password)
			request.user.save()
			user = authenticate(username=request.user.username, password=password)
			login(request, user)
			return redirect('/profile/'+user.username+'/')
		return render(request, 'core/settings.html', {'profile':detalhes})

def edit_details_profile(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		detalhes = get_object_or_404(Profile, user=request.user)
		form = EditProfile(request.POST or None, instance=detalhes)
		if form.is_valid():
			detalhes = form.save(commit=False)
			var = detalhes.imagem_perfil
			detalhes.imagem_perfil = request.FILES.get('imagem_perfil', False)
			print detalhes.imagem_perfil
			if detalhes.imagem_perfil != False:
				file_type = detalhes.imagem_perfil.url.split('.')[-1]
				file_type = file_type.lower()
				if file_type not in FILE_TYPES_IMAGE:
					detalhes.imagem_perfil = None
					return render(request, 'core/edit_profile.html', {'form':form, 'user':request.user, 'avisoimagem':'Formato de imagem inválido.', 'profile':detalhes})
			else:
				detalhes.imagem_perfil = var
			bio = form.cleaned_data['bio']
			githut = form.cleaned_data['git']
			#haha pegadinha do Django kkkk (ManyToManyField não considera alterações sem salvar a instância)
			detalhes.habilidades = form.cleaned_data['habilidades']
			if detalhes.habilidades.count() > 5:
				detalhes.habilidades.clear()
				hab = get_object_or_404(Areas,nome_linguagem='Outra linguagem')
				detalhes.habilidades.add(hab)
				return render(request, 'core/edit_profile.html', {'form': form, 'user':request.user, 'aviso':'Escolha até 5 habilidades!', 'profile':detalhes})
			detalhes.ativo = True
			detalhes.save()
			return profile(request, request.user.username)
	return render(request, 'core/edit_profile.html', {'form': form, 'user':request.user, 'profile':detalhes})

def profile(request, username):
	use = get_object_or_404(User, username=username)
	participations = Participations.objects.filter(user=use)
	favorites = Favorites.objects.filter(user=use)
	profile = get_object_or_404(Profile, user=use)

	instanciaSeguidor = Followers()
	instanciaBlock = Blocked()

	dadoBlock = 0

	if request.user.is_authenticated():
		perfil = get_object_or_404(Profile, user=request.user)
		if perfil.ativo == False:
			return edit_details_profile(request)
		dadosSeguir = instanciaSeguidor.get_dados_seguidor(request.user, use)
		dadosSDV = instanciaSeguidor.get_dados_seguidor(use, request.user)
		eu = get_object_or_404(Profile, user=request.user)
		data_comecou_seguir = instanciaSeguidor.get_data_que_comecou_seguir(request.user, use)
		
		dadoBlock = instanciaBlock.get_dados_esta_block(request.user, use)

	else:
		dadosSeguir = dadosSDV = 0
		eu = data_comecou_seguir = None
	followings = instanciaSeguidor.relacao_de_seguindo_decrescente(use)
	followers = instanciaSeguidor.relacao_de_seguidores_decrescente(use)


	posts = Post.objects.filter(user=use, exibir_perfil=True)

	paginator = Paginator(posts[::-1], 5)
	page = request.GET.get('page')
	print(page)
	print("Estou requisitando a {} página" .format(page))

	try:
		relations = paginator.page(page)
		print(relations)
	except PageNotAnInteger:
		relations = paginator.page(1)
	except EmptyPage:
		relations = paginator.page(paginator.num_pages)
	return render(request, 'core/profile.html', {
		'relations':relations, 'profile':profile,
		'participations':participations,
		'favorites':favorites,
		'dadosSeguir':dadosSeguir,
		'dadosSDV':dadosSDV,
		'eu':eu,
		'data':data_comecou_seguir,
		'numerofollowings':followings,
		'numerofollowers':followers,
		'dadoBlock':dadoBlock})

def friendsactivities(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		eu = get_object_or_404(Profile, user=request.user)
		if eu.ativo == False:
			return edit_details_profile(request)
		instanciaFollowers = Followers()
		dados = instanciaFollowers.get_timeline_friends_activities(instanciaFollowers.relacao_de_seguindo_decrescente(request.user))
		
		paginator = Paginator(dados, 10)
		page = request.GET.get('page')
		print(page)
		print("Estou requisitando a {} página" .format(page))

		try:
			relations = paginator.page(page)
			print(relations)
		except PageNotAnInteger:
			relations = paginator.page(1)
		except EmptyPage:
			relations = paginator.page(paginator.num_pages)

		return render(request, 'core/friendsactivities.html', {'dados': relations, 'eu':eu})

def atualizaVisto(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		usuario = get_object_or_404(Profile, user=request.user)
		instanciaProfile = Profile()
		instanciaProfile.atualiza_visto(usuario)
		return HttpResponse(json.dumps("Visto por ultimo deste usuário atualizado"), content_type="application/json")

def verificaDispo(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		if request.method == 'POST':
			pkprofile = request.POST.get('id')
			profile = get_object_or_404(Profile, pk=pkprofile)
			instanciaProfile = Profile()
			diferenca = instanciaProfile.verificaDispo(profile)
			print diferenca
			return HttpResponse(json.dumps(str(diferenca)), content_type="application/json")
		return HttpResponse(json.dumps(False), content_type="application/json")


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['senha']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'core/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'core/login.html', {'error_message': 'Invalid login'})
    return render(request, 'core/login.html')

def logout_user(request):
	logout(request)
	return render(request, 'core/login.html')

def create_fix(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		eu = get_object_or_404(Profile, user=request.user)
		if eu.ativo == False:
			return edit_details_profile(request)
		fixie = Fixies()
		fixie.save()
		form = FixiesForm(request.POST or None, instance=fixie)
		if form.is_valid():
			fixie = form.save(commit=False)
			fixie.user = request.user
			fixie.area = form.cleaned_data['area']

			if fixie.area.count() > 5 or fixie.area.count() == 0:
				fixie.area.clear()
				hab = get_object_or_404(Areas,nome_linguagem='Outra linguagem')
				fixie.area.add(hab)
			fixie.save()
			return redirect('/')
		fixie.delete()
		return render(request, 'core/createfix.html', {'form':form, 'eu':eu})

def fix_detail(request, pk, aviso=False):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')

	else:
		eu = get_object_or_404(Profile, user=request.user)
		if eu.ativo == False:
			return edit_details_profile(request)
		form = ComentForm(request.POST or None)
		if form.is_valid():
			com = form.save(commit=False)
			coment = form.cleaned_data['coment']
			com.user = request.user
			com.fixie = Fixies.objects.get(pk=pk)
			if com.fixie.user != request.user:
				if com.fixie.ativa_notificacao != False:
					com.fixie.notificacao += 1
					com.fixie.save()
					coment = form.cleaned_data['coment']
			try:
				table_participation = Participations.objects.get(user=request.user, fixie=com.fixie)
				print("tabela já existe")
			except ObjectDoesNotExist:
				if com.fixie.user != request.user:
					table_participation = Participations()
					table_participation.user=request.user
					table_participation.fixie = com.fixie
					table_participation.save()
					print("tabela ainda não existe")
					print("Objetos relacionados")

			#----------------------------------
			#O laço for seguinte notifica os usuários que se relacionaram com o fix
			#--------------------------------------
			ids_participantes = []
			table = Participations.objects.filter(fixie=com.fixie)
			for t in table:
				#ids_participantes.append(t.user.pk)
				relationship = Participations.objects.get(user=t.user, fixie=com.fixie)
				if relationship.user != request.user and relationship.user != com.fixie.user:
					if relationship.ativa_notificacao != False:
						relationship.notificacao += 1
						relationship.save()
			#print(ids_participantes)

			#-----------------------------
			#O laço for seguinte notifica os usuários que favoritaram o fix
			#--------------------------------------
			ids_pessoas_que_favoritaram_este_fix = []
			table_fix = Favorites.objects.filter(fixie=com.fixie)
			for tf in table_fix:
				relationship_favorites = Favorites.objects.get(user=tf.user, fixie=com.fixie)
				if relationship_favorites.user != request.user:
					relationship_favorites.notificacao += 1
					relationship_favorites.save()


			com.save()
			return redirect('/fix/'+pk+'/#post')
		fixie = get_object_or_404(Fixies, pk=pk)
		if fixie.user == request.user:
			print('este fix é deste usuario')
			fixie.notificacao = 0
			fixie.save()
			chave = True
		else:
			print('este fix não é deste usuario')
			chave = False

		try:
			table_participation = Participations.objects.get(user=request.user, fixie=fixie)
			if table_participation:
				if table_participation.ativa_notificacao == True:
					chave_de_participacao = 1
				else:
					chave_de_participacao = 2
				table_participation.notificacao = 0
				table_participation.save()
				print("tabela já existe, é participação deste usuário e as notificações desta participação foram zeradas")
		except ObjectDoesNotExist:
			chave_de_participacao = 0
			print("Este usuário não tem participação com este fixie")

		try:
			table_fav = Favorites.objects.get(user=request.user, fixie=fixie)
			if table_fav:
				table_fav.notificacao = 0
				table_fav.save()
				print("tabela já existe, é favoritado deste usuário e as notificações desta relação foram zeradas")
		except ObjectDoesNotExist:
			print("Este usuário não tem relação de favorito com este fixie")

		if fixie.user != request.user:
			try:
				table_favorite = Favorites.objects.get(user=request.user, fixie=fixie)
				if table_favorite:
					print("este fix é favorito deste usuário")
					chave_fav = 1
			except ObjectDoesNotExist:
				print("este fix não é favorito deste usuário")
				chave_fav = 2
		else:
			chave_fav = 0

		instanciaBlock = Blocked()
		acessoBlock = False
		if instanciaBlock.get_dados_esta_block(fixie.user, request.user) == 1:
			acessoBlock = True

		coments = ComentFixies.objects.filter(fixie=fixie.pk)
	return render(request, 'core/fixdetail.html', {'eu': eu,'fixie': fixie, 'coments':coments, 'form':form, 'chave':chave, 'chave_fav':chave_fav, 'aviso':aviso, 'chave_de_participacao':chave_de_participacao, 'acessoBlock':acessoBlock })

def best_answer(request, pk):
	#ufa! essa view quase me mata kkk :')
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:

		if request.method == 'POST':
			comentpk = request.POST.get('id')
			fixie = get_object_or_404(Fixies, pk=pk)
			response_data = "Deu errado"
			if fixie.user != request.user:
				print('este fix não é deste usuario')
				raise Http404
			else:
				lista = []
				coments = ComentFixies.objects.filter(fixie=fixie.pk)
				for com in coments:
					lista.append(int(com.pk))

				if int(comentpk) not in lista:
					print("indice de coments invalido para exte fixie")
					raise Http404
				else:
					for com in coments:
						if com.melhor_resposta == True:
							com.melhor_resposta = False
							com.save()
							print "Salvou"

					newmybestanswer = get_object_or_404(ComentFixies, pk=comentpk)
					newmybestanswer.melhor_resposta = True
					newmybestanswer.save()
					fixie.tem_melhor_resposta = True
					fixie.save()
					response_data = "Deu certo"
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")


def mark_fixed_code(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:

		if request.method == 'POST':
			fix = request.POST.get('id')
			fixie = get_object_or_404(Fixies, pk=fix)
			response_data = "Deu errado"
			if fixie.user != request.user:
				print('este fix não é deste usuario')
				raise Http404
			elif fixie.tem_melhor_resposta:
				fixie.resolvido = True
				fixie.save()
				response_data = "Deu certo"
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")


def confirm_delete_fix(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		if request.method == 'POST':
			use = request.POST.get('id')
			fixie = get_object_or_404(Fixies, pk=pk)
			response_data = {}
			if fixie.user != request.user:
				print('este fix não é deste usuario')
				raise Http404
			else:
				fixie.delete()
				print("chegou pra deletar")
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")


def to_restore_fixed_code(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:

		if request.method == 'POST':
			fix = request.POST.get('id')
			fixie = get_object_or_404(Fixies, pk=fix)
			response_data = "Deu errado"
			if fixie.user != request.user:
				print('este fix não é deste usuario')
				raise Http404
			elif fixie.tem_melhor_resposta:
				fixie.resolvido = False
				fixie.save()
				response_data = "Deu certo"
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")

def my_fixies(request, delete=False):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:		
		eu = get_object_or_404(Profile, user=request.user)
		if eu.ativo == False:
			return edit_details_profile(request)
		instanciaFixies = Fixies()
		fixies = instanciaFixies.get_todos_fixies_sem_notificacao(request.user)
		paginator = Paginator(fixies, 5)

		page = request.GET.get('page')
		try:
			pagina = paginator.page(page)
		except PageNotAnInteger:
			pagina = paginator.page(1)
		except EmptyPage:
			pagina = paginator.page(paginator.num_pages)
		return render(request, 'core/myfixies.html', {'pagina': pagina, 'delete':delete, 'eu':eu})

def my_fixiesN(request, delete=False):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:		
		eu = get_object_or_404(Profile, user=request.user)
		if eu.ativo == False:
			return edit_details_profile(request)
		instanciaFixies = Fixies()
		fixies = instanciaFixies.get_fixies_com_novas_respostas(request.user)
		paginator = Paginator(fixies, 5)

		page = request.GET.get('page')
		try:
			pagina = paginator.page(page)
		except PageNotAnInteger:
			pagina = paginator.page(1)
		except EmptyPage:
			pagina = paginator.page(paginator.num_pages)
		return render(request, 'core/myfixiesN.html', {'pagina': pagina, 'delete':delete, 'eu':eu})

def participationsSemUser(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:		
		eu = get_object_or_404(Profile, user=request.user)
		if eu.ativo == False:
			return edit_details_profile(request)
		instanciaParticipation = Participations()
		participations = instanciaParticipation.get_participations_sem_notificacao(request.user)
		paginator = Paginator(participations, 5)

		page = request.GET.get('page')
		try:
			pagina = paginator.page(page)
		except PageNotAnInteger:
			pagina = paginator.page(1)
		except EmptyPage:
			pagina = paginator.page(paginator.num_pages)
		return render(request, 'core/myparticipations.html', {'pagina':pagina, 'eu':eu})

def participationsSemUserN(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:		
		eu = get_object_or_404(Profile, user=request.user)
		if eu.ativo == False:
			return edit_details_profile(request)
		instanciaParticipation = Participations()
		participations = instanciaParticipation.get_participations_com_novas_respostas(request.user)
		paginator = Paginator(participations, 5)

		page = request.GET.get('page')
		try:
			pagina = paginator.page(page)
		except PageNotAnInteger:
			pagina = paginator.page(1)
		except EmptyPage:
			pagina = paginator.page(paginator.num_pages)
		return render(request, 'core/myparticipationsN.html', {'pagina':pagina, 'eu':eu})

def favoritesSemUser(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:		
		eu = get_object_or_404(Profile, user=request.user)
		if eu.ativo == False:
			return edit_details_profile(request)
		instanciaFavorites = Favorites()
		participations = instanciaFavorites.get_favorites_sem_notificacao(request.user)
		paginator = Paginator(participations, 5)

		page = request.GET.get('page')
		try:
			pagina = paginator.page(page)
		except PageNotAnInteger:
			pagina = paginator.page(1)
		except EmptyPage:
			pagina = paginator.page(paginator.num_pages)
		return render(request, 'core/myfavorites.html', {'pagina':pagina, 'eu':eu})

def favoritesSemUserN(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:		
		eu = get_object_or_404(Profile, user=request.user)
		if eu.ativo == False:
			return edit_details_profile(request)
		instanciaFavorites = Favorites()
		participations = instanciaFavorites.get_favorites_com_novas_respostas(request.user)
		paginator = Paginator(participations, 5)

		page = request.GET.get('page')
		try:
			pagina = paginator.page(page)
		except PageNotAnInteger:
			pagina = paginator.page(1)
		except EmptyPage:
			pagina = paginator.page(paginator.num_pages)
		return render(request, 'core/myfavoritesN.html', {'pagina':pagina, 'eu':eu})

def inativeNotifyMyFixies(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		relacao = get_object_or_404(Fixies, user=request.user, pk=pk)
		if relacao.user == request.user:
			relacao.ativa_notificacao = False
			relacao.save()
		else:
			raise Http404
		return fix_detail(request, pk)

def ativeNotifyMyFixies(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		if request.method == 'POST':
			pk = request.POST.get('id')
			fixie = get_object_or_404(Fixies, pk=pk)
			if fixie.user == request.user:
				fixie.ativa_notificacao = True
				fixie.save()
				response_data = "Notificações ativadas"
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")

def inativeNotifyMyFixies(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		if request.method == 'POST':
			pk = request.POST.get('id')
			fixie = get_object_or_404(Fixies, pk=pk)
			if fixie.user == request.user:
				fixie.ativa_notificacao = False
				fixie.save()
				response_data = "Notificações desativadas"
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")


def participations(request, username):
	use = get_object_or_404(User, username=username)
	participations = Participations.objects.filter(user=use)
	favorites = Favorites.objects.filter(user=use)
	profile = get_object_or_404(Profile, user=use)

	instanciaSeguidor = Followers()

	instanciaBlock = Blocked()
	dadoBlock = 0

	if request.user.is_authenticated():
		dadosSeguir = instanciaSeguidor.get_dados_seguidor(request.user, use)
		dadosSDV = instanciaSeguidor.get_dados_seguidor(use, request.user)
		eu = get_object_or_404(Profile, user=request.user)
		data_comecou_seguir = instanciaSeguidor.get_data_que_comecou_seguir(request.user, use)
		dadoBlock = instanciaBlock.get_dados_esta_block(request.user, use)
	else:
		dadosSeguir = dadosSDV = 0
		eu = data_comecou_seguir = None

	followings = instanciaSeguidor.relacao_de_seguindo_decrescente(use)
	followers = instanciaSeguidor.relacao_de_seguidores_decrescente(use)

	paginator = Paginator(participations[::-1], 5)
	page = request.GET.get('page')
	print(page)
	print("Estou requisitando a {} página" .format(page))

	try:
		relations = paginator.page(page)
		print(relations)
	except PageNotAnInteger:
		relations = paginator.page(1)
	except EmptyPage:
		relations = paginator.page(paginator.num_pages)
	return render(request, 'core/participations.html', {
		'relations':relations, 'profile':profile,
		'participations':participations,
		'favorites':favorites,
		'dadosSeguir':dadosSeguir,
		'dadosSDV':dadosSDV,
		'eu':eu,
		'data':data_comecou_seguir,
		'numerofollowings':followings,
		'numerofollowers':followers,
		'dadoBlock':dadoBlock})


def getnotifyparticipation(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		response_data = False
		if request.method == 'POST':
			pkfix = request.POST.get('id')
			fixie = get_object_or_404(Fixies, pk=pkfix)
			if fixie.user == request.user:
				raise Http404
			relacao = get_object_or_404(Participations, user=request.user, fixie=fixie)
			if relacao.ativa_notificacao == True:
				response_data = True
			else:
				response_data = False
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")

def ativeNotifyParticipations(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		response_data = False
		if request.method == 'POST':
			pkfix = request.POST.get('id')
			fixie = get_object_or_404(Fixies, pk=pkfix)
			relacao = get_object_or_404(Participations, user=request.user, fixie=fixie)
			relacao.ativa_notificacao = True
			relacao.save()
			response_data = True
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")

def inativeNotifyParticipations(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		response_data = False
		if request.method == 'POST':
			pkfix = request.POST.get('id')
			fixie = get_object_or_404(Fixies, pk=pkfix)
			relacao = get_object_or_404(Participations, user=request.user, fixie=fixie)
			relacao.ativa_notificacao = False
			relacao.save()
			response_data = True
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")

def deleteParticipation(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		response_data = False
		if request.method == 'POST':
			pkfix = request.POST.get('id')
			fixie = get_object_or_404(Fixies, pk=pkfix)
			if fixie.user == request.user:
				print "entrou no if de erro"
				raise Http404
			relacao = get_object_or_404(Participations, user=request.user, fixie=fixie)
			relacao.delete()
			response_data = True
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")

def getRelationshipFavorite(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		response_data = False
		if request.method == 'POST':
			pkfix = request.POST.get('id')
			fixie = get_object_or_404(Fixies, pk=pkfix)
			if fixie.user != request.user:
				try:
					fav = Favorites.objects.get(user=request.user, fixie=fixie)
					if fav:
						response_data = True
				except ObjectDoesNotExist:
					response_data = False
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")

def favorite_fix(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		response_data = "Nao favoritou"
		if request.method == 'POST':
			pkfix = request.POST.get('id')
			fixie = get_object_or_404(Fixies, pk=pkfix)
			if fixie.user != request.user:
				table_favorite = Favorites()
				table_favorite.user = request.user
				table_favorite.fixie = fixie
				table_favorite.save()
				print("relacionamento criado")
				response_data = "favoritou"
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")

def favorite_fix(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		response_data = "Nao favoritou"
		if request.method == 'POST':
			pkfix = request.POST.get('id')
			fixie = get_object_or_404(Fixies, pk=pkfix)
			if fixie.user != request.user:
				try:
					table_favorite = Favorites()
					table_favorite.user = request.user
					table_favorite.fixie = fixie
					table_favorite.save()
					print("relacionamento criado")
					response_data = "favoritou"
				except ObjectDoesNotExist:
					response_data = "Nao favoritou"
					raise Http404
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")

def un_favorite_fix(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		response_data = "Nao desfavoritou"
		if request.method == 'POST':
			pkfix = request.POST.get('id')
			fixie = get_object_or_404(Fixies, pk=pkfix)
			if fixie.user != request.user:
				try:
					table_favorite = Favorites.objects.get(user=request.user, fixie=fixie)
					if table_favorite:
						print("este fix já é favorito deste usuário")
						table_favorite.delete()
						response_data = "desfavoritou"
				except ObjectDoesNotExist:
					print("este fix não é favorito deste usuário")
					raise Http404
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")


def favorites(request, username):
	use = get_object_or_404(User, username=username)
	participations = Participations.objects.filter(user=use)
	favorites = Favorites.objects.filter(user=use)
	profile = get_object_or_404(Profile, user=use)

	instanciaSeguidor = Followers()

	instanciaBlock = Blocked()
	dadoBlock = 0

	if request.user.is_authenticated():
		dadosSeguir = instanciaSeguidor.get_dados_seguidor(request.user, use)
		dadosSDV = instanciaSeguidor.get_dados_seguidor(use, request.user)
		eu = get_object_or_404(Profile, user=request.user)
		data_comecou_seguir = instanciaSeguidor.get_data_que_comecou_seguir(request.user, use)
		dadoBlock = instanciaBlock.get_dados_esta_block(request.user, use)
	else:
		dadosSeguir = dadosSDV = 0
		eu = data_comecou_seguir = None

	followings = instanciaSeguidor.relacao_de_seguindo_decrescente(use)
	followers = instanciaSeguidor.relacao_de_seguidores_decrescente(use)

	paginator = Paginator(favorites[::-1], 5)
	page = request.GET.get('page')
	print(page)
	print("Estou requisitando a {} página" .format(page))

	try:
		relations = paginator.page(page)
		print(relations)
	except PageNotAnInteger:
		relations = paginator.page(1)
	except EmptyPage:
		relations = paginator.page(paginator.num_pages)
	return render(request, 'core/favorites.html', {
		'relations':relations, 'profile':profile,
		'participations':participations,
		'favorites':favorites,
		'dadosSeguir':dadosSeguir,
		'dadosSDV':dadosSDV,
		'eu':eu,
		'data':data_comecou_seguir,
		'numerofollowings':followings,
		'numerofollowers':followers,
		'nfollowings':followings[0:9],
		'nfollowers':followers[0:9],
		'dadoBlock':dadoBlock})


def followajax(request, username):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		if request.method == 'POST':
			use = request.POST.get('id')
			userfollow = get_object_or_404(User, username=use)
			response_data = {}
			if userfollow != request.user:
				try:
					procurarRegistro = Followers.objects.get(user=request.user, following=userfollow)
					if procurarRegistro:
						print("{} já segue {}".format(user.username, following.username))
				except ObjectDoesNotExist:
					novoRegistro = Followers()
					novoRegistro.user = request.user
					novoRegistro.following = userfollow
					novoRegistro.save()

					response_data['result'] = 'Usuário seguido com sucesso'
					print("Registro criado")
			return HttpResponse(json.dumps(response_data), content_type="application/json")
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")

def unfollowajax(request, username):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		if request.method == 'POST':
			use = request.POST.get('id')
			userfollow = get_object_or_404(User, username=use)
			response_data = {}
			if userfollow != request.user:
				try:
					procurarRegistro = Followers.objects.get(user=request.user, following=userfollow)
					procurarRegistro.delete()
					print("Parou de seguir")
				except ObjectDoesNotExist:
					raise Http404
			return HttpResponse(json.dumps(response_data), content_type="application/json")
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")


def getrelationship(request, username):
	print "Chegou na função"

	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		if request.method == 'POST':
			use = request.POST.get('id')
			print("o use é: {}".format(use))
			userfollow = get_object_or_404(User, username=use)
			response_data = False
			if userfollow != request.user:
				try:
					procurarRegistro = Followers.objects.get(user=request.user, following=userfollow)
					if procurarRegistro:
						response_data = True
				except ObjectDoesNotExist:
					response_data = False
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")

def getnotifymyfix(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		if request.method == 'POST':
			pk = request.POST.get('id')
			fixie = get_object_or_404(Fixies, pk=pk)
			response_data = False
			if fixie.user == request.user:
				if fixie.ativa_notificacao == True:
					response_data = True
				else:
					response_data = False
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")

def follower(request, username):
	use = get_object_or_404(User, username=username)
	participations = Participations.objects.filter(user=use)
	favorites = Favorites.objects.filter(user=use)
	profile = get_object_or_404(Profile, user=use)

	instanciaSeguidor = Followers()

	instanciaBlock = Blocked()

	dadoBlock = 0

	if request.user.is_authenticated():
		dadosSeguir = instanciaSeguidor.get_dados_seguidor(request.user, use)
		dadosSDV = instanciaSeguidor.get_dados_seguidor(use, request.user)
		eu = get_object_or_404(Profile, user=request.user)
		data_comecou_seguir = instanciaSeguidor.get_data_que_comecou_seguir(request.user, use)
		dadoBlock = instanciaBlock.get_dados_esta_block(request.user, use)
	else:
		dadosSeguir = dadosSDV = 0
		eu = data_comecou_seguir = None

	followings = instanciaSeguidor.relacao_de_seguindo_decrescente(use)
	followers = instanciaSeguidor.relacao_de_seguidores_decrescente(use)

	paginator = Paginator(followers[::-1], 12)
	page = request.GET.get('page')
	print(page)
	print("Estou requisitando a {} página" .format(page))

	try:
		relations = paginator.page(page)
		print(relations)
	except PageNotAnInteger:
		relations = paginator.page(1)
	except EmptyPage:
		relations = paginator.page(paginator.num_pages)
	return render(request, 'core/followers.html', {
		'relations':relations, 'profile':profile,
		'participations':participations,
		'favorites':favorites,
		'dadosSeguir':dadosSeguir,
		'dadosSDV':dadosSDV,
		'eu':eu,
		'data':data_comecou_seguir,
		'numerofollowings':followings,
		'numerofollowers':followers,
		'dadoBlock':dadoBlock})

def following(request, username):
	use = get_object_or_404(User, username=username)
	participations = Participations.objects.filter(user=use)
	favorites = Favorites.objects.filter(user=use)
	profile = get_object_or_404(Profile, user=use)

	instanciaSeguidor = Followers()
	instanciaBlock = Blocked()

	dadoBlock = 0

	if request.user.is_authenticated():
		dadosSeguir = instanciaSeguidor.get_dados_seguidor(request.user, use)
		dadosSDV = instanciaSeguidor.get_dados_seguidor(use, request.user)
		eu = get_object_or_404(Profile, user=request.user)
		data_comecou_seguir = instanciaSeguidor.get_data_que_comecou_seguir(request.user, use)
		dadoBlock = instanciaBlock.get_dados_esta_block(request.user, use)
	else:
		dadosSeguir = dadosSDV = 0
		eu = data_comecou_seguir = None

	followings = instanciaSeguidor.relacao_de_seguindo_decrescente(use)
	followers = instanciaSeguidor.relacao_de_seguidores_decrescente(use)

	paginator = Paginator(followings[::-1], 12)
	page = request.GET.get('page')
	print(page)
	print("Estou requisitando a {} página" .format(page))

	try:
		relations = paginator.page(page)
		print(relations)
	except PageNotAnInteger:
		relations = paginator.page(1)
	except EmptyPage:
		relations = paginator.page(paginator.num_pages)
	return render(request, 'core/following.html', {
		'relations':relations, 'profile':profile,
		'participations':participations,
		'favorites':favorites,
		'dadosSeguir':dadosSeguir,
		'dadosSDV':dadosSDV,
		'eu':eu,
		'data':data_comecou_seguir,
		'numerofollowings':followings,
		'numerofollowers':followers,
		'dadoBlock':dadoBlock})

def lista_bloqueados(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		eu = get_object_or_404(Profile, user=request.user)
		if eu.ativo == False:
			return edit_details_profile(request)
		instanciaBlock = Blocked()
		lista = instanciaBlock.relacao_de_bloqueados_decrescente(request.user)
		return render(request, 'core/blockedlist.html', {'eu':eu, 'lista':lista})

def bloquear_user(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		if request.method == 'POST':
			pkuser = request.POST.get('id')
			user = get_object_or_404(User, username=pkuser)
			instanciaBlock = Blocked()
			response_data = instanciaBlock.bloquear(request.user, user)
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")

def desbloquear_user(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		if request.method == 'POST':
			pkuser = request.POST.get('id')
			user = get_object_or_404(User, username=pkuser)
			instanciaBlock = Blocked()
			response_data = instanciaBlock.desbloquear(request.user, user)
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")

def report_coment(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		if request.method == 'POST':
			comentpk = request.POST.get('id')
			fixie = get_object_or_404(Fixies, pk=pk)
			response_data = "Não foi possível reportar"
			if fixie.user == request.user:
				print("este fix é deste usuário")
				coment = get_object_or_404(ComentFixies, pk=comentpk)
				if coment.user == request.user:
					raise Http404
				else:
					coment.delete()
					response_data = "Reportado com sucesso"
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")


#################################################################################
#Sistema de blog
#################################################################################

def create_post(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		eu = get_object_or_404(Profile, user=request.user)
		if eu.ativo == False:
			return edit_details_profile(request)
		post = Post()
		post.save()
		form = PostForm(request.POST or None, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.user = request.user
			post.anexo = request.FILES.get('anexo', False)
			print post.anexo
			if post.anexo != False:
				print "Usuário upou algo!"
				file_type = post.anexo.url.split('.')[-1]
				file_type = file_type.lower()
				if file_type not in FILE_TYPES:
					return render(request, 'core/createpost.html', {'form':form, 'error_message':'Arquivo inválido', 'eu':eu})
			post.area = form.cleaned_data['area']
			if post.area.count() > 5 or post.area.count() == 0:
				post.area.clear()
				hab = get_object_or_404(Areas,nome_linguagem='Outra linguagem')
				post.area.add(hab)
			post.save()
			return redirect('/post/'+str(post.pk)+'/')
		post.delete()
		return render(request, 'core/createpost.html', {'form':form, 'eu':eu})

def post_detail(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		eu = get_object_or_404(Profile, user=request.user)
		if eu.ativo == False:
			return edit_details_profile(request)

		form = ComentPostForm(request.POST or None)
		if form.is_valid():
			com = form.save(commit=False)
			coment = form.cleaned_data['coment']
			com.user = request.user
			com.post = Post.objects.get(pk=pk)
			if com.post.user != request.user:
				if com.post.ativa_notificacao != False:
					com.post.notificacao += 1
					com.post.save()
					coment = form.cleaned_data['coment']
			com.save()
			return redirect('/post/'+pk+'/#post')

		post = get_object_or_404(Post, pk=pk)
		donoDoPost = get_object_or_404(Profile, user=post.user)

		if post.user == request.user:
			print('este fix é deste usuario')
			post.notificacao = 0
			post.save()
		coments = ComentPost.objects.filter(post=post)

		instanciaBlock = Blocked()

		acessoBlock = False
		if instanciaBlock.get_dados_esta_block(post.user, request.user) == 1:
			acessoBlock = True

		return render(request, 'core/postdetail.html', {'post': post, 'coments':coments, 'form':form, 'eu':eu, 'donoDoPost':donoDoPost, 'acessoBlock':acessoBlock })

def my_posts(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:		
		eu = get_object_or_404(Profile, user=request.user)
		if eu.ativo == False:
			return edit_details_profile(request)
		posts = Post.objects.filter(user=request.user)
		paginator = Paginator(posts[::-1], 5)
		page = request.GET.get('page')
		print(page)
		print("Estou requisitando a {} página" .format(page))

		try:
			pagina = paginator.page(page)
			print(pagina)
		except PageNotAnInteger:
			pagina = paginator.page(1)
		except EmptyPagepagina:
			pagina = paginator.page(paginator.num_pages)
		return render(request, 'core/myposts.html', {'pagina':pagina, 'eu':eu})

def my_postsN(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:		
		eu = get_object_or_404(Profile, user=request.user)
		if eu.ativo == False:
			return edit_details_profile(request)
		instanciaPost = Post()
		lista = instanciaPost.get_posts_notificados(request.user)

		paginator = Paginator(lista, 5)
		page = request.GET.get('page')
		print(page)
		print("Estou requisitando a {} página" .format(page))

		try:
			pagina = paginator.page(page)
			print(pagina)
		except PageNotAnInteger:
			pagina = paginator.page(1)
		except EmptyPage:
			pagina = paginator.page(paginator.num_pages)
		return render(request, 'core/mypostsN.html', {'pagina':pagina, 'eu':eu})

def getkeypostprofile(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		if request.method == 'POST':
			pk = request.POST.get('id')
			post = get_object_or_404(Post, pk=pk)
			response_data = False
			if post.user == request.user:
				if post.exibir_perfil == True:
					response_data = True
				else:
					response_data = False
			else:
				raise Http404
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")

def ativepostprofile(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		if request.method == 'POST':
			pk = request.POST.get('id')
			post = get_object_or_404(Post, pk=pk)
			response_data = False
			if post.user == request.user:
				post.exibir_perfil = True
				post.save()
				response_data = True
			else:
				raise Http404
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")

def inativepostprofile(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		if request.method == 'POST':
			pk = request.POST.get('id')
			post = get_object_or_404(Post, pk=pk)
			response_data = False
			if post.user == request.user:
				post.exibir_perfil = False
				post.save()
				response_data = True
			else:
				raise Http404
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")

def edit_post(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		eu = get_object_or_404(Profile, user=request.user)
		if eu.ativo == False:
			return edit_details_profile(request)
		post = get_object_or_404(Post, pk=pk)
		if post.user == request.user:
			form = PostForm(request.POST or None, instance=post)
			if form.is_valid():
				post = form.save(commit=False)
				post.user = request.user
				var = post.anexo
				post.anexo = request.FILES.get('anexo', False)
				print post.anexo
				if post.anexo != False:
					print "O usuário postou algo!"
					file_type = post.anexo.url.split('.')[-1]
					file_type = file_type.lower()
					if file_type not in FILE_TYPES:
						return render(request, 'core/editpost.html', {'form':form, 'error_message':'Arquivo inválido', 'edit':True, 'post':post, 'eu':eu})
				else:
					post.anexo = var
				post.save()
				return redirect('/post/'+pk+'/')
			return render(request, 'core/editpost.html', {'form':form, 'edit':True, 'post':post, 'eu':eu})
		else:
			raise Http404

def delete_post(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		if request.method == 'POST':
			idPost = request.POST.get('id')
			post = get_object_or_404(Post, pk=idPost)
			response_data = False
			if post.user != request.user:
				print('este fix não é deste usuario')
				raise Http404
			else:
				post.delete()
				print("chegou pra deletar")
				response_data = True
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")

def getkeyactivepost(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		if request.method == 'POST':
			pk = request.POST.get('id')
			post = get_object_or_404(Post, pk=pk)
			response_data = False
			if post.user == request.user:
				if post.ativa_notificacao == True:
					response_data = True
				else:
					response_data = False
			else:
				raise Http404
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")

def ativeNotifyPost(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		if request.method == 'POST':
			pk = request.POST.get('id')
			post = get_object_or_404(Post, pk=pk)
			response_data = False
			if post.user == request.user:
				post.ativa_notificacao = True
				post.save()
				response_data = True
			else:
				raise Http404
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")

def inativeNotifyPost(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		if request.method == 'POST':
			pk = request.POST.get('id')
			post = get_object_or_404(Post, pk=pk)
			response_data = False
			if post.user == request.user:
				post.ativa_notificacao = False
				post.save()
				response_data = True
			else:
				raise Http404
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")

def report_coment_post(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		if request.method == 'POST':
			comentpk = request.POST.get('id')
			post = get_object_or_404(Post, pk=pk)
			response_data = "Não foi possível reportar"
			if post.user == request.user:
				print("este fix é deste usuário")
				coment = get_object_or_404(ComentPost, pk=comentpk)
				coment.delete()
				response_data = "Comentário reportado com sucesso"
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")


def sala(request, pkreceptor):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		eu = get_object_or_404(Profile, user=request.user)
		if eu.ativo == False:
			return edit_details_profile(request)
		instanciaMessage = Message()
		instanciaBlock = Blocked()
		userVisitado = get_object_or_404(User, pk=pkreceptor)
		profileVisitado = get_object_or_404(Profile, user=userVisitado)
		if request.user == userVisitado:
			return render(request, 'core/conversaAlone.html', {'eu':eu})
		mensagens = instanciaMessage.get_20_messages(request.user, userVisitado)

		blockInfo = False

		if instanciaBlock.get_dados_esta_block(userVisitado, request.user) == 1:
			blockInfo = 1
		elif instanciaBlock.get_dados_esta_block(request.user, userVisitado) == 1:
			blockInfo = 2

		return render(request, 'core/conversa.html', {'mensagens':mensagens, 'userVisitado':userVisitado, 'profileVisitado':profileVisitado, 'eu':eu, 'blockInfo':blockInfo})


def messages_not_view(request, pkreceptor):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		instanciaMessage = Message()
		userVisitado = get_object_or_404(User, pk=pkreceptor)
		if request.user == userVisitado:
			return render(request, 'core/conversaAlone.html')
		mensagens = instanciaMessage.get_messages_not_view(request.user, userVisitado)
		print(mensagens)
		return HttpResponse(json.dumps(mensagens), content_type="application/json")

def all_messages(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		if request.method == 'POST':
			away = request.POST.get('id')
			instanciaMessage = Message()
			userVisitado = get_object_or_404(User, pk=away)
			if request.user == userVisitado:
				return render(request, 'core/conversaAlone.html')
			resultado = instanciaMessage.get_all_messages(request.user, userVisitado)
			return HttpResponse(json.dumps(resultado), content_type="application/json")
		return HttpResponse(json.dumps(False), content_type="application/json")

def read_messages(request, pkreceptor):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		instanciaMessage = Message()
		userVisitado = get_object_or_404(User, pk=pkreceptor)
		instanciaBlock = Blocked()
		if instanciaBlock.get_dados_esta_block(userVisitado, request.user) == 1 or instanciaBlock.get_dados_esta_block(request.user, userVisitado) == 1:
			raise Http404
		if request.user == userVisitado:
			return render(request, 'core/conversaAlone.html')
		mensagens = instanciaMessage.set_le_mensagens(request.user, userVisitado)
		print(mensagens)
		return HttpResponse(json.dumps("Mensagens lidas com sucesso"), content_type="application/json")

def send_message(request, pkreceptor):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		if request.method == 'POST':
			mensagem = request.POST.get('id')
			print mensagem
			instanciaMessage = Message()
			userVisitado = get_object_or_404(User, pk=pkreceptor)
			if request.user == userVisitado:
				return render(request, 'core/conversaAlone.html')
			resultado = instanciaMessage.send_message(request.user, userVisitado, mensagem)
			return HttpResponse(json.dumps(resultado), content_type="application/json")
		return HttpResponse(json.dumps(False), content_type="application/json")

def verifica_leitura(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		if request.method == 'POST':
			idvi = request.POST.get('id')
			instanciaMessage = Message()
			userVisitado = get_object_or_404(User, pk=idvi)
			if request.user == userVisitado:
				return render(request, 'core/conversaAlone.html')
			resultado = instanciaMessage.verifica_leitura_de_msg(request.user, userVisitado)
			return HttpResponse(json.dumps(resultado), content_type="application/json")
		return HttpResponse(json.dumps(False), content_type="application/json")

def deleta_conversa(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		if request.method == 'POST':
			idvi = request.POST.get('id')
			instanciaMessage = Message()
			userVisitado = get_object_or_404(User, pk=idvi)
			if request.user == userVisitado:
				return render(request, 'core/conversaAlone.html')
			resultado = instanciaMessage.delete_messages(request.user, userVisitado)
			return HttpResponse(json.dumps(resultado), content_type="application/json")
		return HttpResponse(json.dumps(False), content_type="application/json")

def my_contacts(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		eu = get_object_or_404(Profile, user=request.user)
		if eu.ativo == False:
			return edit_details_profile(request)
		instanciaMessage = Message()
		instanciaSeguidor = Followers()
		quantidade_mensagens = instanciaMessage.count_messages(request.user)
		contatos_recentes = instanciaMessage.get_users_recently(request.user)
		lista_seguindo = instanciaSeguidor.relacao_de_seguindo_decrescente(request.user)
		return render(request, 'core/mycontacts.html', {'eu':eu, 'quantidade_mensagens':quantidade_mensagens, 'contatos_recentes':contatos_recentes, 'lista_seguindo':lista_seguindo})

def search_area_fix(request, linguagem):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		eu = get_object_or_404(Profile, user=request.user)
		instanciaArea = Areas()
		area = get_object_or_404(Areas, pk=linguagem)

		paginator = Paginator(instanciaArea.busca_fix(area), 5)
		page = request.GET.get('page')
		print(page)
		print("Estou requisitando a {} página" .format(page))

		try:
			pagina = paginator.page(page)
			print(pagina)
		except PageNotAnInteger:
			pagina = paginator.page(1)
		except EmptyPagepagina:
			pagina = paginator.page(paginator.num_pages)
		return render(request, 'core/areafix.html', {'eu':eu, 'pagina':pagina, 'area':area, 'habilidades':eu.habilidades.all()})

def search_area_post(request, linguagem):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		eu = get_object_or_404(Profile, user=request.user)
		instanciaArea = Areas()
		area = get_object_or_404(Areas, pk=linguagem)

		paginator = Paginator(instanciaArea.busca_post(area), 5)
		page = request.GET.get('page')
		print(page)
		print("Estou requisitando a {} página" .format(page))

		try:
			pagina = paginator.page(page)
			print(pagina)
		except PageNotAnInteger:
			pagina = paginator.page(1)
		except EmptyPagepagina:
			pagina = paginator.page(paginator.num_pages)
		return render(request, 'core/areapost.html', {'eu':eu, 'pagina':pagina, 'area':area, 'habilidades':eu.habilidades.all()})

def search_area_user(request, linguagem):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		eu = get_object_or_404(Profile, user=request.user)
		instanciaArea = Areas()
		area = get_object_or_404(Areas, pk=linguagem)

		paginator = Paginator(instanciaArea.busca_user(area), 24)
		page = request.GET.get('page')
		print(page)
		print("Estou requisitando a {} página" .format(page))

		try:
			pagina = paginator.page(page)
			print(pagina)
		except PageNotAnInteger:
			pagina = paginator.page(1)
		except EmptyPagepagina:
			pagina = paginator.page(paginator.num_pages)
		return render(request, 'core/areausers.html', {'eu':eu, 'pagina':pagina, 'area':area, 'habilidades':eu.habilidades.all()})

def search_fix(request, argumento):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		eu = get_object_or_404(Profile, user=request.user)
		instanciaFixies = Fixies()
		resultado = instanciaFixies.search_fix(argumento)

		paginator = Paginator(resultado, 5)
		page = request.GET.get('page')
		print(page)
		print("Estou requisitando a {} página" .format(page))

		try:
			pagina = paginator.page(page)
			print(pagina)
		except PageNotAnInteger:
			pagina = paginator.page(1)
		except EmptyPagepagina:
			pagina = paginator.page(paginator.num_pages)
		return render(request, 'core/searchfix.html', {'eu':eu, 'pagina':pagina, 'argumento':argumento})

def search_post(request, argumento):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		eu = get_object_or_404(Profile, user=request.user)
		instanciaPost = Post()
		resultado = instanciaPost.search_post(argumento)

		paginator = Paginator(resultado, 5)
		page = request.GET.get('page')
		print(page)
		print("Estou requisitando a {} página" .format(page))

		try:
			pagina = paginator.page(page)
			print(pagina)
		except PageNotAnInteger:
			pagina = paginator.page(1)
		except EmptyPagepagina:
			pagina = paginator.page(paginator.num_pages)
		return render(request, 'core/searchpost.html', {'eu':eu, 'pagina':pagina, 'argumento':argumento})

def search_user(request, argumento):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		eu = get_object_or_404(Profile, user=request.user)
		instanciaProfile = Profile()
		resultado = instanciaProfile.search_user(argumento)

		paginator = Paginator(resultado, 30)
		page = request.GET.get('page')
		print(page)
		print("Estou requisitando a {} página" .format(page))

		try:
			pagina = paginator.page(page)
			print(pagina)
		except PageNotAnInteger:
			pagina = paginator.page(1)
		except EmptyPagepagina:
			pagina = paginator.page(paginator.num_pages)
		return render(request, 'core/searchuser.html', {'eu':eu, 'pagina':pagina, 'argumento':argumento})


def anon_feedback(request):
	if not request.user.is_authenticated():
		form = FeedbackForm(request.POST or None)
		if form.is_valid():
			user = form.save()
			user.save()
			return render(request, 'core/feedbackSuccess.html')
		return render(request, 'core/feedback.html', {'form':form})
	else:
		raise Http404

#Verificação de expert

def verifica_exp(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		profile = get_object_or_404(Profile, user=request.user)
		if profile.expert == True or profile.ativo == False:
			return False
		else:
			lista = list()
			if profile.imagem_perfil:
				lista.append(profile.imagem_perfil.url)
			lista.append(request.user.first_name)
		return HttpResponse(json.dumps(lista), content_type="application/json")
	return HttpResponse(json.dumps(False), content_type="application/json")

def comecar(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		profile = get_object_or_404(Profile, user=request.user)
		profile.expert = True
		profile.save()	
		return HttpResponse(json.dumps(True), content_type="application/json")
	return HttpResponse(json.dumps(False), content_type="application/json")