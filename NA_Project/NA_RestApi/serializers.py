from rest_framework import serializers
from NA_WebApp.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'title', 'prepTime', 'cookTime', 'difficulity', 'description')




