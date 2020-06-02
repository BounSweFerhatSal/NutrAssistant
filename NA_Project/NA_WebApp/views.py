from django.http import HttpResponse
from django.shortcuts import render
import json


def home(request):
    # return HttpResponse('<h1>Blog Home Page</h1>')
    # context = {'posts': posts} // the data ( get it from db / models )
    # return render(request, 'blogapp/home.html', context)

    if request.user.is_authenticated:
        # Do something for authenticated users.

        return render(request, 'NA_WebApp/_homeuser.html', {'title': 'Title of the blog'})

    else:
        # Do something for anonymous users.
        return render(request, 'NA_WebApp/_home.html', {'title': 'Title of the blog'})


def recipes(request):
    return render(request, 'NA_WebApp/recipes.html', {'data': 'pass the value'})


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


def diseaseSearch(request):
    res = [
        {'label': 'Java', 'value': 1},
        {'label': 'Java1', 'value': 2},
        {'label': 'Java2', 'value': 3},
    ]

    prm = request.POST.get('term', '')
    if prm == 'new':
        res = []

    return HttpResponse(json.dumps(res))


def diseaseAddNew(request):
    prm = request.POST.get('term', '')
    # add this to db here
    res = {'label': prm, 'value': 145}
    return HttpResponse(json.dumps(res))
