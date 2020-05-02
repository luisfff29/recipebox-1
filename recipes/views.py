from django.shortcuts import render, get_object_or_404
from recipes.models import Source, Recipe


def index(request):
    recipes = Recipe.objects.all().order_by('title')
    return render(request, 'recipes/index.html', {'recipes': recipes, })


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe_ingredients = recipe.ingredients.split('\n')
    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'recipe_ingredients': recipe_ingredients})


def source_detail(request, pk):
    source = get_object_or_404(Source, pk=pk)
    recipes = Recipe.objects.filter(
        source=source).order_by('title')
    return render(request, 'recipes/source_detail.html', {
        'source': source, 'recipes': recipes})
