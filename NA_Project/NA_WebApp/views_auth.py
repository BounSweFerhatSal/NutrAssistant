from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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
    form = UserCreationForm(request.POST)
    if request.method == 'GET':
        return render(request, 'NA_WebApp/auth/register.html', {'form': form,'hideErrors' : 'true'})
    elif request.method == 'POST':

        # Actually I did not send an html data using this 'form thing'
        # instead I used the theme's screen but I modified the names of the fields as what they has to be
        # for gathering a UserCreationForm from the html posted
        # and add a hidden username field as a trick which is equal to email field ! Yep I'm not so clever !
        # why : because it is much easier to validate the form using this thing.
        # and it checks if a user already exits etc ...
        uname = ""
        firstname = ""
        lastname = ""
        passw = ""



        if form.is_valid():
            # we should do something like this :   form.save() ,
            # yes this is a short cut but I do not want to fight with user creation form modifying !

            uname = form.cleaned_data.get('username')  # yep this is the trick !
            firstname = request.POST.get('first_name')
            lastname = request.POST.get('last_name')
            passw = form.cleaned_data.get('password1')

            user = User.objects.create_user(uname, uname, passw)
            # At this point, user is a User object that has already been saved to the database.
            # but we can continue to change its attributes:
            user.first_name = firstname
            user.last_name = lastname
            user.save()

            # I should add the email confirmation functionality and set is_active to false after then :
            # user.is_active = false
            # sending email code will be here :
            # .....
            # .....
            login(request, user)
            messages.success(request, 'Welcome '
                             + firstname + ' ' + lastname)
            return redirect('NA_WebApp-home')

        # Here we send the form data to template just for showing the errors
        # Otherwise we had to create a message with a loop in errors and send it to template
        return render(request, 'NA_WebApp/auth/register.html',

                      {'form': form, 'uname': uname, 'firstname': firstname, 'lastname': lastname})

def forget(request):
    return render(request, 'NA_WebApp/auth/forget.html', {'title': 'Title of the blog'})

def signout(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'NA_WebApp/_home.html', {'title': 'Title of the blog'})
