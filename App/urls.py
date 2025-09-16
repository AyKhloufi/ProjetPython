from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name="recipe_detail"),
    path('ingredients/', views.IngredientListView.as_view(), name="ingredients"),
    path('ingredients/add/', views.AddIngredientView.as_view(), name="add_ingredient"),
    path('recipes/add/', views.AddRecipeView.as_view(), name="add_recipe"),
    path('quantity_units/', views.QuantityUnitListView.as_view(), name="quantity_units"),
    path('quantity_unit/add/', views.AddQuantityUnitView.as_view(), name="add_quantity_unit"),
    path('recipes/<int:pk>/edit/', views.EditRecipeView.as_view(), name="edit_recipe"),
    path('recipes/<int:pk>/delete/', views.DeleteRecipeView.as_view(), name="delete_recipe"),
    path('ingredients/<int:pk>/edit/', views.EditIngredientView.as_view(), name="edit_ingredient"),
    path('ingredients/<int:pk>/delete/', views.DeleteIngredientView.as_view(), name="delete_ingredient"),
    path('quantity_units/<int:pk>/edit/', views.EditQuantityUnitView.as_view(), name="edit_quantity_unit"),
    path('quantity_units/<int:pk>/delete/', views.DeleteQuantityUnitView.as_view(), name="delete_quantity_unit"),
]
