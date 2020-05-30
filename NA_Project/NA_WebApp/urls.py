from django.urls import path
from . import views
from . import views_auth

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [path('', views.home, name='NA_WebApp-home'),
               path('auth/login', views_auth.signin, name='NA_WebApp-login'),
               path('auth/logout', views_auth.signout, name='NA_WebApp-logout'),
               path('auth/forget', views_auth.forget, name='NA_WebApp-forget'),
               path('auth/register', views_auth.register, name='NA_WebApp-register'),
               path('auth/profile', views_auth.profile, name='NA_WebApp-profile'),
               path('recipes/', views.recipes, name='NA_WebApp-recipes'),
               path('enjoy/', views.frontendtest, name='NA_WebApp-enjoy'),
               path('enjoy/ajaxget', views.ajax_getdata_test, name='NA_WebApp-ajaxget'),
               path('enjoy/ajaxpost', views.ajax_getdata_test, name='NA_WebApp-ajaxpost'),
               ]

