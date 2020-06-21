from django import forms
from .models import Profile, Recipe


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'height', 'weight', 'gender', 'birthYear', 'married', 'hasKids', 'lat', 'lng']


class RecipeCreateForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'prepTime', 'cookTime', 'portions',
                  'difficulity']
