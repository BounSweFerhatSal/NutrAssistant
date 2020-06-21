import requests
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view

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
        return JsonResponse({"error": str(e)}, safe=False)


@api_view(['POST'])
def GetNutrients(request):
    try:

        if request.method == 'POST':
            ingredientId = request.POST['ingredientId']

            # we will return the Portions :
            portions = []

            # check if we already have this in db :
            ingredient = Ingredient.objects.get(FDC_ID=ingredientId)
            if ingredient is not None:
                ing_portions = Ingredient_Portions.objects.filter(ingredient_id=ingredientId)
                for p in ing_portions:
                    portions.append({'value': p.portion.id, 'text': p.portion.name})

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

                    # first check if we have this nutrient in db, if not create it
                    if Nutrient.objects.get(FDC_ID=nutrient['id']) is None:
                        Nutrient.objects.create(FDC_ID=nutrient['id'],
                                                name=nutrient['name'])

                    # check if we have this ingredient_Composition in db, if not create it
                    if Ingredient_Composition.objects.get(ingredient_id=ingredientId, nutrient_id=nutrient['id']) is None:
                        Ingredient_Composition.objects.create(ingredient_id=ingredientId,
                                                              nutrient_id=nutrient['id'],
                                                              amount=nutrient['amount'],
                                                              unitname=nutrient['unitName'])

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
                    if Portion.objects.get(FDC_ID=portionId) is None:
                        Portion.objects.create(FDC_ID=portionId,
                                               name=portionName,
                                               gramWeight=portionWeight)

                    # Check if we have this Ingredient_Portions in db, if not create it
                    if Ingredient_Portions.objects.get(ingredient_id=ingredientId, portion_id=portionId):
                        Ingredient_Portions.objects.create(ingredient_id=ingredientId,
                                                           portion_id=portionId)

                    # now add to list to return :
                    portions.append({'value': portionId, 'text': portionName})

                return JsonResponse(portions, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, safe=False)


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
