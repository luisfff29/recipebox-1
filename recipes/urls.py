
from django.urls import path
from recipes import views

urlpatterns = [
    path('', views.index, name='home'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('source/<int:pk>/', views.source_detail, name='source_detail'),
    path('addsource/', views.add_source, name='add_source'),
    path('addrecipe/', views.add_recipe, name='add_recipe'),
]
