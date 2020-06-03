from django.shortcuts import (
    render, get_object_or_404, reverse, HttpResponseRedirect)
from recipes.models import Author, Recipe
from recipes.forms import (AddAuthorForm,
                           StaffAddRecipeForm,
                           UserAddRecipeForm,
                           LoginForm)
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied


def index(request):
    recipes = Recipe.objects.all().order_by('title')
    return render(request, 'recipes/index.html', {'recipes': recipes, })


@staff_member_required(login_url='/login/?next=/addauthor/')
def add_author(request):
    html = "recipes/add_form.html"
    message_before = """Create a new user/author below.
      Each user account is associates with exactly one author name."""
    if request.method == "POST":
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            User.objects.create_user(
                username=data['username'],
                password=data['password']
            )
            Author.objects.create(
                name=data['author_name'],
                bio=data['bio'],
                user=User.objects.get(username=data['username'])
            )
        return HttpResponseRedirect(reverse('home'))
    form = AddAuthorForm()
    return render(request, html, {
        'form': form, 'message_before': message_before})


@login_required
def add_recipe(request):
    html = "recipes/add_form.html"
    if request.user.is_staff:
        if request.method == "POST":
            form = StaffAddRecipeForm(request.POST)
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
        form = StaffAddRecipeForm()
        return render(request, html, {
            'form': form,
        })
    else:
        if request.method == "POST":
            form = UserAddRecipeForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                Recipe.objects.create(
                    title=data['title'],
                    author=Author.objects.get(name=request.user.author),
                    description=data['description'],
                    time_required=data['time_required'],
                    instructions=data['instructions'],
                )
            return HttpResponseRedirect(reverse('home'))
        form = UserAddRecipeForm()
        return render(request, html, {
            'form': form,
        })


@login_required
def update_recipe(request, pk):
    html = "recipes/add_form.html"
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user.is_staff:
        if request.method == "POST":
            form = StaffAddRecipeForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                recipe.title = data['title']
                recipe.author = data['author']
                recipe.description = data['description']
                recipe.time_required = data['time_required']
                recipe.instructions = data['instructions']
            recipe.save()
            return HttpResponseRedirect(reverse('recipe_detail', args=(pk, )))

        form = StaffAddRecipeForm(initial={
            'title': recipe.title,
            'author': recipe.author,
            'description': recipe.description,
            'time_required': recipe.time_required,
            'instructions': recipe.instructions
        })
        return render(request, html, {'form': form})
    elif request.user.author == recipe.author:
        if request.method == "POST":
            form = UserAddRecipeForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                recipe.title = data['title']
                recipe.description = data['description']
                recipe.time_required = data['time_required']
                recipe.instructions = data['instructions']
            recipe.save()
            return HttpResponseRedirect(reverse('recipe_detail', args=(pk, )))

        form = UserAddRecipeForm(initial={
            'title': recipe.title,
            'description': recipe.description,
            'time_required': recipe.time_required,
            'instructions': recipe.instructions
        })
        return render(request, html, {'form': form})
    else:
        raise PermissionDenied
        # You don't currently have permission to update or edit this recipe.


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe, })


def favorite_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    try:
        author = Author.objects.get(user=request.user)
    except Exception as e:
        print(e)
        return HttpResponseRedirect(reverse('recipe_detail', args=(pk, )))
    recipe.favorites.add(author)
    return HttpResponseRedirect(reverse('recipe_detail', args=(pk, )))


def unfavorite_recipe(request, pk):
    pass


def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    recipes = Recipe.objects.filter(
        author=author).order_by('title')
    return render(request, 'recipes/author_detail.html', {
        'author': author, 'recipes': recipes, })


def loginview(request):
    message_after = ""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get('next', reverse('home'))
                )
            else:
                message_after = """Credentials supplied do not match our records.
                    Please try again."""
    form = LoginForm()
    return render(request, 'recipes/add_form.html',
                  {'form': form, 'message_after': message_after})


@login_required()
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.GET.get('next', reverse('home')))
