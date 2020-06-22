from django.urls import path
from . import views, views_auth, views_defs, views_recipe

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [path('', views.home, name='NA_WebApp-home'),
               path('auth/login', views_auth.signin, name='NA_WebApp-login'),
               path('auth/logout', views_auth.signout, name='NA_WebApp-logout'),
               path('auth/forget', views_auth.forget, name='NA_WebApp-forget'),
               path('auth/register', views_auth.register, name='NA_WebApp-register'),
               path('auth/profile', views_auth.profile, name='NA_WebApp-profile'),
               path('auth/profile_preferences', views_auth.profile_preferences, name='NA_WebApp-preferences'),

               path('recipes/', views.recipes, name='NA_WebApp-recipes'),

               path('enjoy/', views.frontendtest, name='NA_WebApp-enjoy'),
               path('enjoy/ajaxget', views.ajax_getdata_test, name='NA_WebApp-ajaxget'),
               path('enjoy/ajaxpost', views.ajax_getdata_test, name='NA_WebApp-ajaxpost'),

               path('auth/diseaseSearch', views_defs.diseaseSearch, name='NA_WebApp-diseaseSearch'),
               path('auth/diseaseAddNew', views_defs.diseaseAddNew, name='NA_WebApp-diseaseAddNew'),
               path('auth/search_allergies', views_defs.search_allergies, name='NA_WebApp-search_allergies'),
               path('auth/add_allergy', views_defs.add_allergy, name='NA_WebApp-add_allergy'),
               path('auth/search_labels', views_defs.search_labels, name='NA_WebApp-search_allergies'),
               path('auth/add_label', views_defs.add_label, name='NA_WebApp-add_allergy'),
               path('auth/search_ingredients', views_defs.search_ingredients, name='NA_WebApp-search_ingredients'),
               path('auth/add_ingredient', views_defs.add_ingredient, name='NA_WebApp-add_ingredient'),

               path('recipe/recipe_create', views_recipe.recipe_create, name='NA_WebApp-recipe_create'),
               path('recipe/recipeAddIngredient', views_recipe.recipeAddIngredient, name='NA_WebApp-recipeAddIngredient'),
               path('recipe/recipeDeleteIngredient', views_recipe.recipeDeleteIngredient , name='NA_WebApp-recipeDeleteIngredient'),
               path('recipe/recipeUpdateInstructions', views_recipe.recipeUpdateInstructions, name='NA_WebApp-recipeUpdateInstructions'),

               ]
