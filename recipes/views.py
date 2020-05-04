from django.shortcuts import (
    render, get_object_or_404, reverse, HttpResponseRedirect)
from recipes.models import Source, Recipe
# from django.utils import forms
from recipes.forms import AddSourceForm, AddRecipeForm


def index(request):
    recipes = Recipe.objects.all().order_by('title')
    return render(request, 'recipes/index.html', {'recipes': recipes, })


def add_source(request):
    html = "recipes/add_form.html"
    if request.method == "POST":
        form = AddSourceForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse('home'))
    form = AddSourceForm()
    return render(request, html, {'form': form})


def add_recipe(request):
    html = "recipes/add_form.html"
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse('home'))
    form = AddRecipeForm()
    return render(request, html, {'form': form})


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
