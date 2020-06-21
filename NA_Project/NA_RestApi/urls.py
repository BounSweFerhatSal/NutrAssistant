from django.urls import path
from . import views

urlpatterns = [
    path('getFoods/', views.GetFoods, name='NA_RestApi-GetFoods'),
    path('getNutrients/', views.GetNutrients, name='NA_RestApi-GetNutrients'),
    path('test/subfolder', views.testsubfolder, name='NA_RestApi-testsubfolder'),

]
