from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import Profile, Recipe


def show_profile(request):
    uid = request.GET['profileid']
    if Profile.objects.filter(id=uid).count() > 0:

        profile = Profile.objects.get(id=uid)
        recipes = Recipe.objects.filter(user_id=profile.user_id)
        return render(request, 'NA_WebApp/social/public_profile.html', {'profile': profile, 'recipes': recipes})
    else:
        return render(request, 'NA_WebApp/Error.html', {'errorcode': '500', 'errorname': 'Internal Server', 'errortext': 'There is no profile with this  ID : (' + uid + ')'})
