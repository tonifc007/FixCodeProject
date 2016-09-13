# -*- coding: utf 8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from .models import Fixies, ComentFixies, Participations, Favorites
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, FixiesForm, ComentForm
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def index(request):
	if not request.user.is_authenticated():
		print("foi no if")
		return render(request, 'core/login.html')
	else:
		print("saiu no if")
		fixies = Fixies.objects.all()
		myfixies = Fixies.objects.filter(user=request.user)
		count_notify = 0
		for fix in myfixies:
			if int(fix.notificacao) > 0:
				count_notify += 1

		myrelationships = Participations.objects.filter(user=request.user)
		count_notify_relationships = 0
		for mr in myrelationships:
			if int(mr.notificacao) > 0:
				count_notify_relationships += 1

		return render(request, 'core/index.html', {'fixies': fixies, 'count_notify': count_notify, 'count_notify_relationships': count_notify_relationships})

def register(request):
	form = UserForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user.set_password(password)
		user.save()
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				fixies = Fixies.objects.all
				#fixies = Fixies.objects.filter(user=request.user)
				return redirect('/')
	return render(request, 'core/register.html', {'form':form})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['senha']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return index(request)
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
		form = FixiesForm(request.POST or None)
		if form.is_valid():
			fixie = form.save(commit=False)
			fixie.user = request.user
			fixie.save()
			return redirect('/')
		return render(request, 'core/createfix.html', {'form':form})

def fix_detail(request, pk):
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
				com.fixie.notificacao += 1
				com.fixie.save()
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
				table_participation.notificacao = 0
				table_participation.save()
				print("tabela já existe, é participação deste usuário e as notificações desta participação foram zeradas")
		except ObjectDoesNotExist:
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
	return render(request, 'core/fixdetail.html', {'fixie': fixie, 'coments':coments, 'form':form, 'chave': chave, 'chave_fav': chave_fav})

def best_answer(request, fixpk, compk):
	#ufa! essa view quase me mata kkk :')
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		fixie = get_object_or_404(Fixies, pk=fixpk)

		if fixie.user != request.user:
			print('este fix não é deste usuario')
			raise Http404
		else:
			lista = []
			coments = ComentFixies.objects.filter(fixie=fixie.pk)
			for com in coments:
				print(com.pk)
				lista.append(int(com.pk))

			print(compk)
			print(lista)

			if int(compk) not in lista:
				print("indice de coments invalido para exte fixie")
				raise Http404
			else:
				for com in coments:
					com.melhor_resposta = False
					com.save()
				newmybestanswer = get_object_or_404(ComentFixies, pk=compk)
				newmybestanswer.melhor_resposta = True
				newmybestanswer.save()
				fixie.tem_melhor_resposta = True
				fixie.save()
				return fix_detail(request, fixpk)

def mark_fixed_code(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		fixie = get_object_or_404(Fixies, pk=pk)

		if fixie.user != request.user:
			print('este fix não é deste usuario')
			raise Http404
		elif fixie.tem_melhor_resposta:
			fixie.resolvido = True
			fixie.save()
		return fix_detail(request, pk)


def to_restore_fixed_code(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		fixie = get_object_or_404(Fixies, pk=pk)

		if fixie.user != request.user:
			print('este fix não é deste usuario')
			raise Http404
		else:
			fixie.resolvido = False
			fixie.save()
			return fix_detail(request, pk)

def my_fixies(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		fixies = Fixies.objects.filter(user=request.user)
		return render(request, 'core/myfixies.html', {'fixies': fixies})

# def participations(request):
# 	if not request.user.is_authenticated():
# 		return render(request, 'core/login.html')
# 	else:
# 		mycoments = ComentFixies.objects.filter(user=request.user)
# 		relatedfixies = []
# 		for com in mycoments:
# 			if com.fixie.user != request.user:
# 				relatedfixies.append(com.fixie)

# 		return render(request, 'core/participations.html', {'relatedfixies':relatedfixies})

def participations(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		myparticipations = Participations.objects.filter(user=request.user)
		return render(request, 'core/participations.html', {'myparticipations':myparticipations})

def favorite_fix(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		fixie = get_object_or_404(Fixies, pk=pk)
		if fixie.user != request.user:
			try:
				table_favorite = Favorites.objects.get(user=request.user, fixie=fixie)
				if table_favorite:
					print("este fix já é favorito deste usuário")
			except ObjectDoesNotExist:
				print("este fix não é favorito deste usuário")
				table_favorite = Favorites()
				table_favorite.user = request.user
				table_favorite.fixie = fixie
				table_favorite.save()
				print("relacionamento criado")
			return fix_detail(request, pk)
	raise Http404

def un_favorite_fix(request, pk):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		fixie = get_object_or_404(Fixies, pk=pk)
		if fixie.user != request.user:
			try:
				table_favorite = Favorites.objects.get(user=request.user, fixie=fixie)
				if table_favorite:
					print("este fix já é favorito deste usuário")
					table_favorite.delete()
			except ObjectDoesNotExist:
				print("este fix não é favorito deste usuário")
				raise Http404
			return fix_detail(request, pk)
	raise Http404

def favorites(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		myfavorites = Favorites.objects.filter(user=request.user)
		return render(request, 'core/favorites.html', {'myfavorites':myfavorites})