from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Diseases, Allergies, Labels, Ingredient
from django.contrib.auth.decorators import login_required
import json

from .forms import ProfileUpdateForm


@login_required(login_url='/auth/login')
def diseaseSearch(request):
    # we will turn this array
    res = []

    # prm = request.POST.get('term', '')
    query_prm = request.POST.get('term', '')
    query_results = Diseases.objects.filter(diseaseName__istartswith=query_prm)

    if query_results.count() >= 0:
        for r in query_results:
            res.append({'label': r.diseaseName, 'value': r.id})

    return HttpResponse(json.dumps(res))


@login_required(login_url='/auth/login')
def diseaseAddNew(request):
    new_disname = request.POST.get('term', '')

    # add this to db here
    new_dis = Diseases.objects.create(diseaseName=new_disname)

    res = {'label': new_disname, 'value': new_dis.id}
    return HttpResponse(json.dumps(res))


@login_required(login_url='/auth/login')
def search_allergies(request):
    # we will turn this array
    res = []

    # prm = request.POST.get('term', '')
    query_prm = request.POST.get('term', '')
    query_results = Allergies.objects.filter(name__istartswith=query_prm)

    if query_results.count() >= 0:
        for r in query_results:
            res.append({'label': r.name, 'value': r.id})

    return HttpResponse(json.dumps(res))


@login_required(login_url='/auth/login')
def add_allergy(request):
    new_name = request.POST.get('term', '')

    # add this to db here
    new_rec = Allergies.objects.create(name=new_name)

    res = {'label': new_name, 'value': new_rec.id}
    return HttpResponse(json.dumps(res))


@login_required(login_url='/auth/login')
def search_labels(request):
    # we will turn this array
    res = []

    # prm = request.POST.get('term', '')
    query_prm = request.POST.get('term', '')
    query_results = Labels.objects.filter(name__istartswith=query_prm)

    if query_results.count() >= 0:
        for r in query_results:
            res.append({'label': r.name, 'value': r.id})

    return HttpResponse(json.dumps(res))


@login_required(login_url='/auth/login')
def add_label(request):
    new_name = request.POST.get('term', '')

    # add this to db here
    new_rec = Labels.objects.create(name=new_name)

    res = {'label': new_name, 'value': new_rec.id}
    return HttpResponse(json.dumps(res))


@login_required(login_url='/auth/login')
def search_ingredients(request):
    # we will turn this array
    res = []

    # prm = request.POST.get('term', '')
    query_prm = request.POST.get('term', '')
    query_results = Ingredient.objects.filter(name__icontains=query_prm)

    if query_results.count() >= 0:
        for r in query_results:
            res.append({'label': r.name, 'value': r.id})

    return HttpResponse(json.dumps(res))


@login_required(login_url='/auth/login')
def add_ingredient(request):
    new_name = request.POST.get('term', '')
    new_calorie = 100  # request.POST.get('calorie', '')

    # add this to db here
    new_rec = Ingredient.objects.create(name=new_name, calorie=new_calorie, FDC_ID=0)

    res = {'label': new_name, 'value': new_rec.id}
    return HttpResponse(json.dumps(res))
