from django.shortcuts import render
from recipes.models import Source, Recipe


def index(request):
    recipes = Recipe.objects.all()
    sources = Source.objects.all()
    return render(request, 'index.html', {'recipes': recipes,
                                          'sources': sources})
