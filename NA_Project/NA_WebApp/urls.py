from django.urls import path
from . import views

urlpatterns = [path('', views.home, name='NA_WebApp-home'),
               path('recipes/', views.recipes, name='NA_WebApp-recipes'),
               path('enjoy/', views.frontendtest, name='NA_WebApp-enjoy'),
               path('enjoy/ajaxget', views.ajax_getdata_test, name='NA_WebApp-ajaxget'),
               path('enjoy/ajaxpost', views.ajax_getdata_test, name='NA_WebApp-ajaxpost'),
               ]
