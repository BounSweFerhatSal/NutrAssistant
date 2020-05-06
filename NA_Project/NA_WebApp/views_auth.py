from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
import json


def signin(request):
    if request.method == 'GET':
        return render(request, 'NA_WebApp/auth/login.html', {'title': ''})
    elif request.method == 'POST':

        # get email and password data
        uname = request.POST.get('email', '')
        passw = request.POST.get('password', '')
        msg = "not yet"
        # authenticate the user :
        user = authenticate(request, username=uname, password=passw)
        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            msg = "wellcome , your last login was : " + str(user.last_login)
        else:
            # No backend authenticated the credentials
            msg = "ooops ! there is no user sorry !"

        return render(request, 'NA_WebApp/enjoy/responseform.html', {'message': msg})


def register(request):
    return render(request, 'NA_WebApp/auth/register.html', {'title': 'Title of the blog'})


def forget(request):
    return render(request, 'NA_WebApp/auth/forget.html', {'title': 'Title of the blog'})


def signout(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'NA_WebApp/_home.html', {'title': 'Title of the blog'})
