from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view

from NA_RestApi.serializers import RecipeSerializer
from NA_WebApp.models import Recipe


@api_view(['GET', 'POST'])
def test(request):
    if request.method == 'GET':
        x = 5
        # snippets = Snippet.objects.all()
        # serializer = SnippetSerializer(snippets, many=True)
        # return Response(serializer.data)

    recipes = Recipe.objects.all()
    serializer = RecipeSerializer(recipes, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def testsubfolder(request):
    recipes = Recipe.objects.all()
    serializer = RecipeSerializer(recipes, many=True)
    return JsonResponse(serializer.data, safe=False)
