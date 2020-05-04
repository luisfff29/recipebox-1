from django import forms
from recipes.models import Author, Recipe


class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = [
            'name',
            'about',
        ]


class AddRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'author',
            'description',
            'prep_time',
            'cook_time',
            'ingredients',
            'instructions',
            'serves',
        ]
