from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name="recipe_detail"),
    path('ingredients/', views.IngredientListView.as_view(), name="ingredients"),
    path('ingredient/add/', views.AddIngredientView.as_view(), name="add_ingredient"),
    path('recipes/add/', views.AddRecipeView.as_view(), name="add_recipe"),
    path('quantity_units/', views.QuantityUnitListView.as_view(), name="quantity_units"),
    path('quantity_unit/add/', views.AddQuantityUnitView.as_view(), name="add_quantity_unit"),
]
