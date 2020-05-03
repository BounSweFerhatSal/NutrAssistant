from django.urls import path
from . import views

urlpatterns = [path('', views.home, name='NA_WebApp-home'),
               path('recipes/', views.recipes, name='NA_WebApp-recipes'),
               # path('about/', views.about, name='NA_WebApp-about'), //use this to add another route
               ]
