from django.contrib import admin
from .models import Profile,Diseases,Allergies,Labels,Ingredient,Profile_Diseases

admin.site.register(Profile)
admin.site.register(Diseases)
admin.site.register(Allergies)
admin.site.register(Labels)
admin.site.register(Ingredient)
admin.site.register(Profile_Diseases)


