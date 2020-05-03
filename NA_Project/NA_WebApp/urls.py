from django.urls import path from . import views

urlpatterns = [ path('', views.home, name='NA_WebApp-home'),
# path('about/', views.about, name='scwebapp-about'), //use this to add another route
]
