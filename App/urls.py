from django.urls import path
from .views.default_views import *
from .views.default_views import *
from .views.recipe_views import *
from .views.ingredient_views import *
from .views.unit_views import *

urlpatterns = [
    path('', HomeView.as_view(), name="index"),
    path('recipes/', RecipeListView.as_view(), name="recipes"),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name="recipe_detail"),
    path('ingredients/', IngredientListView.as_view(), name="ingredients"),
    path('ingredients/add/', AddIngredientView.as_view(), name="add_ingredient"),
    path('recipes/add/', AddRecipeView.as_view(), name="add_recipe"),
    path('units/', UnitListView.as_view(), name="units"),
    path('units/add/', AddUnitView.as_view(), name="add_unit"),
    path('recipes/<int:pk>/edit/', EditRecipeView.as_view(), name="edit_recipe"),
    path('recipes/<int:pk>/delete/', DeleteRecipeView.as_view(), name="delete_recipe"),
    path('ingredients/<int:pk>/edit/', EditIngredientView.as_view(), name="edit_ingredient"),
    path('ingredients/<int:pk>/delete/', DeleteIngredientView.as_view(), name="delete_ingredient"),
    path('units/<int:pk>/edit/', EditUnitView.as_view(), name="edit_unit"),
    path('units/<int:pk>/delete/', DeleteUnitView.as_view(), name="delete_unit"),
    path('about/', AboutView.as_view(), name="about"),
]
