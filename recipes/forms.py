from django import forms
from recipes.models import Source, Recipe


class AddSourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = [
            'name',
            'about',
        ]


class AddRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'source',
            'description',
            'prep_time',
            'cook_time',
            'ingredients',
            'instructions',
            'serves',
        ]
