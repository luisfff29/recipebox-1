from django.shortcuts import render
from recipes.models import Source, Recipe

sources = Source.objects.all()

# source_recipes = Recipe.objects.filter(source=source).order_by('title')

# <p > {{post.text | linebreaksbr}} < /p >   -- for template


def index(request):
    recipes = Recipe.objects.all().order_by('title')
    return render(request, 'recipes/index.html', {'recipes': recipes, })


# def recipe_detail(request, pk):
#     recipe = Recipe.objects.get(pk)
