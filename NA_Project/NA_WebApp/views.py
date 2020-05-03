from django.http import HttpResponse
from django.shortcuts import render
import json


def home(request):
    # return HttpResponse('<h1>Blog Home Page</h1>')
    # context = {'posts': posts} // the data ( get it from db / models )
    # return render(request, 'blogapp/home.html', context)
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


