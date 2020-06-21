from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test, name='NA_RestApi-test'),
    path('test/subfolder', views.testsubfolder, name='NA_RestApi-testsubfolder'),

]
