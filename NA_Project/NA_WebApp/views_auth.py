from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import json


def signin(request):
    if request.method == 'GET':
        return render(request, 'NA_WebApp/auth/login.html', {'title': ''})
    elif request.method == 'POST':

        # get email and password data
        uname = request.POST.get('email', '')
        passw = request.POST.get('password', '')

        # authenticate the user :
        user = authenticate(request, username=uname, password=passw)
        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            messages.success(request, f'Wellcome {uname}')
            return redirect('NA_WebApp-home')
        else:
            # No backend authenticated the credentials
            messages.error(request, f'Ooops! Username or Password is invalid !')
            return render(request, 'NA_WebApp/auth/login.html', {'uname': uname})



def register(request):
    return render(request, 'NA_WebApp/auth/register.html', {'title': 'Title of the blog'})


def forget(request):
    return render(request, 'NA_WebApp/auth/forget.html', {'title': 'Title of the blog'})


def signout(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'NA_WebApp/_home.html', {'title': 'Title of the blog'})
