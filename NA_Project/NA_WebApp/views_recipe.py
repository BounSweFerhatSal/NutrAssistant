from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .forms import RecipeCreateForm, RecipeImageForm
from .models import Recipe, Ingredient, Recipe_Ingredients, Recipe_Labels, Ingredient_Composition, Nutrient
from django.contrib.auth.decorators import login_required
import json
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.db import connection


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
            return render(request, 'NA_WebApp/recipe/recipe_create.html', {'form': recipe_form, 'recipeId': newrecipe.id, 'done': 'true'})

        else:
            return render(request, 'NA_WebApp/recipe/recipe_create.html', {'form': recipe_form, 'done': 'false'})


@login_required(login_url='/auth/login')
@csrf_protect
def recipeUpdateInstructions(request):
    try:
        if request.method == 'POST':
            r_id = json.loads(request.POST.get('recipeId', ''))
            ins = json.loads(request.POST.get('instructions', ''))

            if Recipe.objects.filter(id=r_id).count() != 0:
                rec = Recipe.objects.get(id=r_id)
                rec.instructions = ins
                rec.save()

                return HttpResponse(json.dumps({'success': 'true'}))

    except Exception as e:
        resp = HttpResponse(json.dumps({"error": str(e)}), content_type="application/json")
        resp.status_code = 500
        return resp


@login_required(login_url='/auth/login')
@csrf_protect
def recipeAddIngredient(request):
    try:

        if request.method == 'POST':
            new_ingredient = json.loads(request.POST.get('new_ingredient', ''))

            same = Recipe_Ingredients.objects.filter(recipe_id=new_ingredient['recipeId'],
                                                     ingredient=Ingredient.objects.get(FDC_ID=new_ingredient['ingredientId'])).count()
            if same != 0:
                resp = HttpResponse(json.dumps({"error": "This Ingredient is already Exists İn This Recipe !"}), content_type="application/json")
                resp.status_code = 500
                return resp

            # add this to db here
            ingObj = Ingredient.objects.get(FDC_ID=new_ingredient['ingredientId'])
            new_rec = Recipe_Ingredients.objects.create(recipe_id=new_ingredient['recipeId'],
                                                        ingredient=ingObj,
                                                        amount=new_ingredient['amount'],
                                                        quantity=new_ingredient['quantity'],
                                                        portion_name=new_ingredient['portion_name']
                                                        )

            return HttpResponse(json.dumps({'success': 'true'}))

    except Exception as e:
        resp = HttpResponse(json.dumps({"error": str(e)}), content_type="application/json")
        resp.status_code = 500
        return resp


@login_required(login_url='/auth/login')
@csrf_protect
def recipeDeleteIngredient(request):
    try:

        if request.method == 'POST':
            del_ingredient = json.loads(request.POST.get('del_ingredient', ''))

            ing = Recipe_Ingredients.objects.filter(recipe_id=del_ingredient['recipeId'],
                                                    ingredient=Ingredient.objects.get(FDC_ID=del_ingredient['ingredientId'])).delete()
            return HttpResponse(json.dumps({'success': 'true'}))

    except Exception as e:
        resp = HttpResponse(json.dumps({"error": str(e)}), content_type="application/json")
        resp.status_code = 500
        return resp


@login_required(login_url='/auth/login')
@csrf_protect
def recipe_updateimage(request):
    if request.method == 'POST':

        if Recipe.objects.filter(id=request.POST['recipe_imageid']).count() > 0:

            rec = Recipe.objects.get(id=request.POST['recipe_imageid'])
            recipe_imageform = RecipeImageForm(request.POST,
                                               request.FILES, instance=rec)

            if recipe_imageform.is_valid():
                recipe_imageform.save()
                return JsonResponse({'error': False, 'filename': request.FILES['photo'].name})
                # return render(request, 'NA_WebApp/recipe/recipe_create.html', {'recipeId': newrecipe.id})
            else:
                return JsonResponse({'error': True, 'errors': recipe_imageform.errors})


@login_required(login_url='/auth/login')
@csrf_protect
def recipe_details(request):
    rid = id = request.GET['recipeId']
    if Recipe.objects.filter(id=rid).count() > 0:
        rec = Recipe.objects.get(id=rid)


        # we are getting nutrient composition of this recipe by raw queries
        # explanataion for : Sum((Ing_com.amount/100) * RI.amount) :
        #                   Ingredeint composiiton table provides the amount of nutritios in this ingredient for 100 grams of the Ingredient
        #                   Recipe Ingredients provides how much ingredient exists in this recipe
        #                   so whe have toc multiply the  RI.amount ( which is grams) with the nutrient amount in the 1 gram of the Ingredient
        #                   therefore :     (Ing_com.amount/100) * RI.amount  gives us nutrient in 1 gram of Ingredient X quaniity of the ongredient in this recipe
        #                   Sum((Ing_com.amount/100) * RI.amount) we are getting the sum of this values of each nutrient in this recipe !

        with connection.cursor() as cursor:
            cursor.execute("SELECT  " +
                           " Ing_com.nutrient_id as N_Id," +
                           " N.name as N_Name," +
                           " Sum((Ing_com.amount/100) * RI.amount) as TotalAmountofNutrient," +
                           " Ing_com.unitname as N_Unit" +
                           " FROM public.\"NA_WebApp_recipe_ingredients\"  as RI" +
                           "              inner join public.\"NA_WebApp_ingredient_composition\" as Ing_com" +
                           "                    on RI.ingredient_id = Ing_com.ingredient_id" +
                           "              inner join public.\"NA_WebApp_nutrient\" as N" +
                           "                    on Ing_com.nutrient_id = N.id" +
                           " WHERE RI.recipe_id= %s" +
                           " GROUP BY Ing_com.nutrient_id,Ing_com.unitname,N.name" +
                           " ORDER BY N_Id", [rid])

            rows = cursor.fetchall()

            nutrient_comp = []
            energy = 0
            for row in rows:
                if row[1] != 'Energy':
                    nut = {'nutrient': row[1],
                           'amount': row[2],
                           'unit': row[3]}

                    nutrient_comp.append(nut)
                else:
                    energy = row[2]




        return render(request, 'NA_WebApp/recipe/recipe_details.html', {'recipe': rec , 'nutrients': nutrient_comp, 'energy' : energy})

    else:
        return render(request, 'NA_WebApp/Error.html', {'errorcode': '500', 'errorname': 'Internal Server', 'errortext': 'There is no recipe with this recipe ID : (' + rid + ')'})
