
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import *
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def userRegister(request):
    if request.method == 'POST':
        user = UserCreationForm(request.POST)
        if user.is_valid():
            user.save()
            messages.success(request,'User has been Created Successfully.')
            return redirect('login')
        else:
            messages.error(request,'Invalid Username or Password')
            return render(request,'auth/register.html',{'form':user})
        
    context= {
        'form': UserCreationForm
    }
    return render(request,'auth/register.html', context)

def userLogin(request):
    if request.method =='POST':
        username = request.POST.get('username') #from forms.py
        password = request.POST.get('password') #from forms.py
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)

            if user.is_staff:
                messages.success(request, f"Welcome {user.username}, You are Logged in.")
                return redirect('/vendor/all-products')
            
            elif user.is_active:
                messages.success(request, f"Welcome {user.username}, You are Logged in.")
                return redirect('/')
        
        else:
            messages.error(request, 'User not found')
            return render(request,'auth/login.html', {'form': LoginForm})


    context={
        'form': LoginForm

    }
    return render(request, 'auth/login.html', context)

def userLogout(request):
    logout(request)
    messages.success(request,"User Logout Success.")
    return redirect('/')
