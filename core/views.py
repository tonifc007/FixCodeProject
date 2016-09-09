from django.shortcuts import render, get_object_or_404, redirect
from .models import Fixies
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm

# Create your views here.

def index(request):
	if not request.user.is_authenticated():
		print("foi no if")
		return render(request, 'core/login.html')
	else:
		print("saiu no if")
		fixies = Fixies.objects.all
		return render(request, 'core/index.html', {'fixies': fixies})

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
				return redirect('core.views.index')
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