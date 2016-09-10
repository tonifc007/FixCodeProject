# -*- coding: utf 8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from .models import Fixies, ComentFixies
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
		return render(request, 'core/index.html', {'fixies': fixies, 'count_notify': count_notify})

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
                fixies = Fixies.objects.all
                return render(request, 'core/index.html', {'fixies': fixies})
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
		coments = ComentFixies.objects.filter(fixie=fixie.pk)
	return render(request, 'core/fixdetail.html', {'fixie': fixie, 'coments':coments, 'form':form, 'chave': chave})

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

def participations(request):
	if not request.user.is_authenticated():
		return render(request, 'core/login.html')
	else:
		mycoments = ComentFixies.objects.filter(user=request.user)
		relatedfixies = []
		for com in mycoments:
			if com.fixie.user != request.user:
				relatedfixies.append(com.fixie)

		return render(request, 'core/participations.html', {'relatedfixies':relatedfixies})
