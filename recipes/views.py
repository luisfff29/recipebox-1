from django.shortcuts import (
    render, get_object_or_404, reverse, HttpResponseRedirect)
from recipes.models import Author, Recipe
from recipes.forms import AddAuthorForm, AddRecipeForm


def index(request):
    recipes = Recipe.objects.all().order_by('title')
    return render(request, 'recipes/index.html', {'recipes': recipes, })


def add_author(request):
    html = "recipes/add_form.html"

    if request.method == "POST":
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Author.objects.create(
                name=data['name'],
                bio=data['bio'],
            )
        return HttpResponseRedirect(reverse('home'))
    form = AddAuthorForm()
    return render(request, html, {'form': form})


def add_recipe(request):
    html = "recipes/add_form.html"
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data['title'],
                author=data['author'],
                description=data['description'],
                time_required=data['time_required'],
                instructions=data['instructions'],
            )
        return HttpResponseRedirect(reverse('home'))
    form = AddRecipeForm()
    return render(request, html, {'form': form})


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe, })


def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    recipes = Recipe.objects.filter(
        author=author).order_by('title')
    return render(request, 'recipes/author_detail.html', {
        'author': author, 'recipes': recipes})
