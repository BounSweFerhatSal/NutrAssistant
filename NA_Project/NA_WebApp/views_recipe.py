from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import RecipeCreateForm
from .models import Recipe, Ingredient, Recipe_Ingredients, Recipe_Labels
from django.contrib.auth.decorators import login_required
import json
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect


@login_required(login_url='/auth/login')
@csrf_protect
def recipe_create(request):
    if request.method == 'GET':

        r_form = RecipeCreateForm()
        return render(request, 'NA_WebApp/recipe/recipe_create.html', {'done': 'false'})

    elif request.method == 'POST':

        recipe_form = RecipeCreateForm(request.POST,
                                       request.FILES)

        if recipe_form.is_valid():
            newrecipe = recipe_form.save()
            messages.success(request, 'Your Recipe is Saved!')
            return render(request, 'NA_WebApp/recipe/recipe_create.html',
                          {'form': recipe_form, 'recipeId': newrecipe.id, 'done': 'true'})
        else:
            return render(request, 'NA_WebApp/recipe/recipe_create.html', {'form': recipe_form, 'done': 'false'})


def recipeAddIngredient(request):
    try:

        if request.method == 'POST':
            new_ingredient = json.loads( request.POST.get('new_ingredient', ''))

            same = Recipe_Ingredients.objects.filter( recipe_id=new_ingredient['recipeId'], ingredient_id=new_ingredient['ingredientId']).count()
            if same != 0:
                resp = HttpResponse(json.dumps({"error": "This Ingredient is already Exists İn This Recipe !"}), content_type="application/json")
                resp.status_code = 500
                return resp

            # add this to db here
            new_rec = Recipe_Ingredients.objects.create(recipe_id=new_ingredient['recipeId'],
                                                        ingredient_id=new_ingredient['ingredientId'],
                                                        amount=new_ingredient['amount'])

            return HttpResponse(json.dumps({'success': 'true'}))

    except Exception as e:
        resp = HttpResponse(json.dumps({"error": str(e)}), content_type="application/json")
        resp.status_code = 500
        return resp


