import decimal

import requests
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from NA_RestApi.serializers import RecipeSerializer
from NA_WebApp.models import Recipe, Ingredient, Ingredient_Composition, Ingredient_Portions, Nutrient, Portion


@api_view(['POST'])
def GetFoods(request):
    try:

        if request.method == 'POST':
            term = request.POST['term']

            USDA_API_KEY = "bKoS8DgKIi1QuIVEEFSmo53h6NSqimhwKvQbVXuh"

            url_get = "https://api.nal.usda.gov/fdc/v1/foods/search?api_key=" + USDA_API_KEY + "&query==" + term

            response = requests.get(url_get)
            searchResults = response.json()

            foods = []
            for food in searchResults['foods']:
                foods.append({'value': food['fdcId'], 'label': food['description']})

            return JsonResponse(foods, safe=False)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def GetNutrients(request):
    try:

        if request.method == 'POST':
            ingredientId = request.POST['ingredientId']

            # we will return the Portions :
            portions = []

            # check if we already have this in db :
            ingredient = Ingredient.objects.filter(FDC_ID=ingredientId)
            if ingredient.count() != 0:
                # we got it , just return the portions :
                ing_portions = Ingredient_Portions.objects.filter(ingredient=Ingredient.objects.get(FDC_ID=ingredientId))
                for p in ing_portions:
                    portions.append({'value': p.portion.id,
                                     'text': p.portion.name + ' (' + str(decimal.Decimal(p.portion.gramWeight).normalize()) + ' gr)', 'gramWeight': p.portion.gramWeight})

                return JsonResponse(portions, safe=False)
            else:
                # Query the USDA , get the nurtients and portions
                USDA_API_KEY = "bKoS8DgKIi1QuIVEEFSmo53h6NSqimhwKvQbVXuh"

                url_get = "https://api.nal.usda.gov/fdc/v1/food/" + ingredientId + "?api_key=" + USDA_API_KEY

                response = requests.get(url_get)
                searchResults = response.json()

                # first get the nutrients
                for foodNutrient in searchResults['foodNutrients']:
                    # to get more info about data structure visit : https://github.com/BounSweFerhatSal/NutrAssistant/wiki/USDA-FDC-API-&-Data-Structure
                    nutrient = foodNutrient['nutrient']

                    # check if we have this nutrient in db, if not create it
                    if Nutrient.objects.filter(FDC_ID=nutrient['id']).count() == 0:
                        Nutrient.objects.create(FDC_ID=nutrient['id'],
                                                name=nutrient['name'])

                    # check if we have this Ingredient in db, if not create it
                    if Ingredient.objects.filter(FDC_ID=ingredientId).count() == 0:
                        Ingredient.objects.create(FDC_ID=ingredientId,
                                                  name=searchResults['description'])

                    # check if we have this ingredient_Composition in db, if not create it
                    if Ingredient_Composition.objects.filter(ingredient_id=ingredientId, nutrient_id=nutrient['id']).count() == 0:

                        if 'amount' in foodNutrient:
                            if foodNutrient['amount'] > 0:

                                Ingredient_Composition.objects.create(ingredient=Ingredient.objects.get(FDC_ID=ingredientId),
                                                                      nutrient=Nutrient.objects.get(FDC_ID=nutrient['id']),
                                                                      amount=foodNutrient['amount'],
                                                                      unitname=nutrient['unitName'])

                                # update the energy value to the ingredient
                                if nutrient['id'] == 1008:  # this the energy !
                                    ing_update = Ingredient.objects.get(FDC_ID=ingredientId)
                                    ing_update.calorie = amount = foodNutrient['amount']
                                    ing_update.save()

                # then get the portions
                for foodPortion in searchResults['foodPortions']:
                    portionId = foodPortion['id']

                    # this is variant :
                    portionName = ""
                    if 'portionDescription' in foodPortion:
                        portionName = foodPortion['portionDescription']
                    else:
                        portionName = foodPortion['modifier']

                    portionWeight = foodPortion['gramWeight']

                    # first check if we have this portion in db, if not create it
                    if Portion.objects.filter(FDC_ID=portionId).count() == 0:
                        Portion.objects.create(FDC_ID=portionId,
                                               name=portionName,
                                               gramWeight=portionWeight)

                    # Check if we have this Ingredient_Portions in db, if not create it
                    if Ingredient_Portions.objects.filter(ingredient_id=ingredientId, portion_id=portionId).count() == 0:
                        Ingredient_Portions.objects.create(ingredient=Ingredient.objects.get(FDC_ID=ingredientId),
                                                           portion=Portion.objects.get(FDC_ID=portionId))

                    # now add to list to return :
                    portions.append({'value': portionId, 'text': portionName + ' (' + str(decimal.Decimal(portionWeight).normalize()) + ' gr)', 'gramWeight': portionWeight})

                return JsonResponse(portions, safe=False)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
def testsubfolder(request):
    recipes = Recipe.objects.all()
    serializer = RecipeSerializer(recipes, many=True)
    return JsonResponse(serializer.data, safe=False)

# post sample:
# url = os.environ.get("URL", 'http://myhost:port/projectname/api/addposition?compName=Google&category=Developer')
# url = "%s" % (url)
# body = {"Company": "%s" % Company, "Position": "%s" % Position}
# response = requests.post(url, auth=HTTPBasicAuth('USER', 'PASSWORD'), headers={'Content-Type': 'application/json'}, json=body)
# if response.status_code == 200:
#     print("Code 200")
# else:
#     print("Code not 200")
