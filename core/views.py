# -*- coding: utf 8 -*-
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Fixies, ComentFixies, Participations, Favorites, Profile, Followers, Post, ComentPost, Areas
from django.contrib.auth import authenticate, login, logout, get_user
from .forms import UserForm, FixiesForm, ComentForm, UserFormRegister, EditProfile, PostForm, ComentPostForm
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
		print("saiu no if")
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

 		#remove todas as duplicatas e ordena por data mais recente
		fixies = sorted(list(set(fixies)), key=lambda inst: inst.data, reverse=True)

		#buscar seguindo pra por na página
		relacao = Followers.objects.filter(user=request.user)
		followings = []

		for pessoa in relacao:
			followings.append(pessoa.following)

		#invertendo para os ultmos serem os primeiros
		followings = followings[::-1]

		

		#sistema de paginação
		paginator = Paginator(fixies, 5)
		page = request.GET.get('page')

		comentariosDosSeguindo = list()
		for i in followings:
			print i.first_name
			comentariosDesteSeguindo = ComentFixies.objects.filter(user=i)
			for a in comentariosDesteSeguindo:
				print("{} coment in {}".format(i.first_name, a.fixie.titulo))
				comentariosDosSeguindo.append(a)

		comentariosDosSeguindo = comentariosDosSeguindo[::-1]
		tempos = list()
		for i in comentariosDosSeguindo:
			tempos.append(timezone.now() - i.data)

		comentariosDosSeguindo = comentariosDosSeguindo[0:10]
		tempos = tempos[0:10]

		try:
			relations = paginator.page(page)
			print(relations)
		except PageNotAnInteger:
			relations = paginator.page(1)
		except EmptyPage:
			relations = paginator.page(paginator.num_pages)

		return render(request, 'core/index.html', {'relations':relations, 'profile':perfil,'comentariosDosSeguindo':comentariosDosSeguindo})

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
			detalhes.save()
			return profile(request, request.user.username)
	return render(request, 'core/edit_profile.html', {'form': form, 'user':request.user, 'profile':detalhes})

def profile(request, username):
	print("Requisitou o perfil de {}".format(username))
	use = get_object_or_404(User, username=username)
	participations = Participations.objects.filter(user=use)
	favorites = Favorites.objects.filter(user=use)
	profile = get_object_or_404(Profile, user=use)
	eu = get_object_or_404(Profile, user=request.user)

	if request.user.is_authenticated():
		dataQueComecouASeguir = None
		if use != request.user:
			try:
				procurarRegistro = Followers.objects.get(user=request.user, following=use)
				if procurarRegistro:
					dadosSeguir = 1
					dataQueComecouASeguir = procurarRegistro.data
			except ObjectDoesNotExist:
				dadosSeguir = 2
		else:
			dadosSeguir = 0

		if use != request.user:
			try:
				procurarRegistroSDV = Followers.objects.get(user=use, following=request.user)
				if procurarRegistroSDV:
					dadosSDV = 1
			except ObjectDoesNotExist:
				dadosSDV = 2
		else:
			dadosSDV = 0
	else:
		dadosSeguir = 0
		dadosSDV = 0

	#buscar seguindo pra por na página
	relacao = Followers.objects.filter(user=use)
	followings = []

	for pessoa in relacao:
		followings.append(pessoa.following)

	#invertendo para os ultmos serem os primeiros
	followings = followings[::-1]

	#formação da matriz 3x3
	matrizDeSeguindo = list()
	for i in range(3):
		matrizDeSeguindo.append(followings[i*3:(i+1)*3])



	#buscar seguidores pra por na pagina
	relacaoSeguidores = Followers.objects.filter(following=use)
	followers = []

	for pessoaS in relacaoSeguidores:
		followers.append(pessoaS.user)

	#invertendo para os ultmos serem os primeiros
	followers = followers[::-1]

	#formação da matriz 3x3
	matrizDeSeguidores = list()
	for i in range(3):
		matrizDeSeguidores.append(followers[i*3:(i+1)*3])

	posts = Post.objects.filter(user=use, exibir_perfil=True)

	paginator = Paginator(posts, 5)
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
		'data':dataQueComecouASeguir,
		'followings':matrizDeSeguindo,
		'nfollowings':followings,
		'followers':matrizDeSeguidores,
		'nfollowers':followers})

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
		return render(request, 'core/createfix.html', {'form':form})

def fix_detail(request, pk, aviso=False):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')

	else:
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

		coments = ComentFixies.objects.filter(fixie=fixie.pk)
	return render(request, 'core/fixdetail.html', {'fixie': fixie, 'coments':coments, 'form':form, 'chave':chave, 'chave_fav':chave_fav, 'aviso':aviso, 'chave_de_participacao':chave_de_participacao})

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
		fixies = Fixies.objects.filter(user=request.user)
		paginator = Paginator(fixies, 5)

		page = request.GET.get('page')
		try:
			pagina = paginator.page(page)
		except PageNotAnInteger:
			pagina = paginator.page(1)
		except EmptyPage:
			pagina = paginator.page(paginator.num_pages)
		return render(request, 'core/myfixies.html', {'pagina': pagina, 'delete':delete})

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
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		user = get_object_or_404(User, username=username)
		myparticipations = Participations.objects.filter(user=user)
		print(user)
		paginator = Paginator(myparticipations, 5)

		if user == request.user:
			chave = True
		else:
			chave = False

		page = request.GET.get('page')
		try:
			pagina = paginator.page(page)
		except PageNotAnInteger:
			pagina = paginator.page(1)
		except EmptyPage:
			pagina = paginator.page(paginator.num_pages)
		return render(request, 'core/participations.html', {'pagina':pagina, 'chave': chave, 'user': user})


def participationsSemUser(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		myparticipations = Participations.objects.filter(user=request.user)
		paginator = Paginator(myparticipations, 5)

		page = request.GET.get('page')
		try:
			pagina = paginator.page(page)
		except PageNotAnInteger:
			pagina = paginator.page(1)
		except EmptyPage:
			pagina = paginator.page(paginator.num_pages)
		return render(request, 'core/participations.html', {'pagina':pagina, 'chave': True, 'user': request.user})


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
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		user = get_object_or_404(User, username=username)
		myfavorites = Favorites.objects.filter(user=user)
		paginator = Paginator(myfavorites, 5)

		if user == request.user:
			chave = True
		else:
			chave = False

		page = request.GET.get('page')
		try:
			pagina = paginator.page(page)
		except PageNotAnInteger:
			pagina = paginator.page(1)
		except EmptyPage:
			pagina = paginator.page(paginator.num_pages)
		return render(request, 'core/favorites.html', {'pagina':pagina, 'chave': chave, 'user': user})


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

def following(request, username):
	userfollow = get_object_or_404(User, username=username)
	relacao = Followers.objects.filter(user=userfollow)
	followings = []

	for pessoa in relacao:
		followings.append(pessoa.following)

	return render(request, 'core/following.html', {'followings':followings, 'userfollow':userfollow})

def follower(request, username):
	userfollow = get_object_or_404(User, username=username)
	relacao = Followers.objects.filter(following=userfollow)

	followers = []

	for pessoa in relacao:
		followers.append(pessoa.user)

	return render(request, 'core/followers.html', {'followers':followers, 'userfollow':userfollow})


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
		post = Post()
		post.save()
		form = PostForm(request.POST or None, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.user = request.user
			post.anexo = request.FILES.get('anexo', False)
			print post.anexo
			if post.anexo != False:
				file_type = post.anexo.url.split('.')[-1]
				file_type = file_type.lower()
				if file_type not in FILE_TYPES:
					return render(request, 'core/createpost.html', {'form':form, 'error_message':'Arquivo inválido'})
			post.area = form.cleaned_data['area']
			if post.area.count() > 5 or post.area.count() == 0:
				post.area.clear()
				hab = get_object_or_404(Areas,nome_linguagem='Outra linguagem')
				post.area.add(hab)
			post.save()
			return redirect('/post/'+str(post.pk)+'/')
		post.delete()
		return render(request, 'core/createpost.html', {'form':form})

def post_detail(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
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

		if post.user == request.user:
			print('este fix é deste usuario')
			post.notificacao = 0
			post.save()
		coments = ComentPost.objects.filter(post=post)

		return render(request, 'core/postdetail.html', {'post': post, 'coments':coments, 'form':form})

def my_posts(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		posts = Post.objects.filter(user=request.user)

		paginator = Paginator(posts, 5)
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
		return render(request, 'core/myposts.html', {'relations':relations})

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
					file_type = post.anexo.url.split('.')[-1]
					file_type = file_type.lower()
					if file_type not in FILE_TYPES:
						return render(request, 'core/createpost.html', {'form':form, 'error_message':'Arquivo inválido'})
				else:
					post.anexo = var
				post.save()
				return redirect('/post/'+pk+'/')
			return render(request, 'core/createpost.html', {'form':form})
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
				if coment.user == request.user:
					raise Http404
				else:
					coment.delete()
					response_data = "Comentário reportado com sucesso"
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")
