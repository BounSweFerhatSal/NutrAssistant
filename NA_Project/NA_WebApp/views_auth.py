from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect

from .forms import ProfileUpdateForm
from .models import Diseases, Allergies, Labels, Ingredient, Profile_Diseases, Profile_Allergies, Profile_FoodPreferences, Profile_RestrictedIngredients, Profile_RestrictedLabels

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
        return render(request, 'NA_WebApp/auth/register.html', {'form': form, 'hideErrors': 'true'})
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


@login_required(login_url='/auth/login')
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if p_form.is_valid():
            p_form.save()
            messages.success(request, 'Your Profile is updated!')
            # post get redirect pattern :
            # to avoid to 'browser ask sure you wonna reload question?'
            # redirect to the page so the browser sends a get request ! brilliant is int it ?
            return redirect('NA_WebApp-profile')



    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    # Here we send the form data to template just for showing the errors
    # Otherwise we had to create a message with a loop in errors and send it to template
    return render(request, 'NA_WebApp/auth/profile.html', {'form': p_form})


@login_required(login_url='/auth/login')
@csrf_protect
def profile_preferences(request):
    try:

        if request.method == 'POST':
            dat = json.loads(request.POST.get('posted_data', ''))

            # get and save the diseases to profile :
            for d in dat['diseases']:
                dis = Diseases.objects.get(id=d)
                if dis is not None:
                    new_rec = Profile_Diseases.objects.create(profile=request.user.profile, disease=dis)  # add this to db here

            # get and save the allergies to profile :
            for a in dat['allergies']:
                alg = Allergies.objects.get(id=a)
                if alg is not None:
                    new_rec = Profile_Allergies.objects.create(profile=request.user.profile, allergy=alg)  # add this to db here

            # get and save the food preferences to profile :
            for fp in dat['foodpreferences']:
                foodp = Labels.objects.get(id=fp)
                if foodp is not None:
                    new_rec = Profile_FoodPreferences.objects.create(profile=request.user.profile, label=foodp)  # add this to db here

            # get and save the RestrictedLabels to profile :
            for aw in dat['awayfrom']:
                restlab = Labels.objects.get(id=aw)
                if restlab is not None:
                    new_rec = Profile_RestrictedLabels.objects.create(profile=request.user.profile, label=restlab)  # add this to db here

            raise Exception("Sorry, no numbers below zero")

            # return HttpResponse(json.dumps(dat), content_type="application/json")
            # messages.success(request, 'Your Preferenes are updated!')
            # return redirect('NA_WebApp-profile')


    except Exception as e:

        resp = HttpResponse(json.dumps({"error": str(e)}), content_type="application/json")
        resp.status_code = 500
        return resp

        # response = JsonResponse({"error": e.message[0:50]})
        # response.status_code = 500  # This is a server side error
        # return response
