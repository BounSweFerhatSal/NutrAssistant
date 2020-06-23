from django.http import HttpResponse
from django.shortcuts import render
from .models import Recipe
from django.contrib.auth.models import User

import json


def home(request):
    # return HttpResponse('<h1>Blog Home Page</h1>')
    # context = {'posts': posts} // the data ( get it from db / models )
    # return render(request, 'blogapp/home.html', context)

    recipe_of_day = Recipe.objects.last()
    last_recipes = Recipe.objects.all()[:6]
    showuser = User.objects.first()
    users = User.objects.all()[:9]

    if request.user.is_authenticated:
        # Do something for authenticated users.

        return render(request, 'NA_WebApp/_homeuser.html', {'recipe': recipe_of_day, 'last': last_recipes, 'usr': showuser, 'users': users})

    else:
        # Do something for anonymous users.
        return render(request, 'NA_WebApp/_home.html', {'recipe': recipe_of_day, 'last': last_recipes, 'usr': showuser, 'users': users})


def error(request):
    return render(request, 'NA_WebApp/Error.html', {'errorcode': '???', 'errorname': '?????', 'errortext': '????????????????'})


def frontendtest(request):
    return render(request, 'NA_WebApp/enjoy/frontendtest.html')


def ajax_getdata_test(request):
    if request.method == 'GET':
        # <view logic>
        return HttpResponse('result is me!')

    elif request.method == 'POST':
        # <view logic>
        sonuc = json.loads(request.POST.get('data', ''))

        return HttpResponse('You Send Me this : ' + sonuc['key1'])
