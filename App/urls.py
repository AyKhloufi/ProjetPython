from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('recipes/', views.RecipeListView.as_view(), name="recipes"),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name="recipe_detail"),
    path('ingredients/', views.IngredientListView.as_view(), name="ingredients"),
    path('ingredients/add/', views.AddIngredientView.as_view(), name="add_ingredient"),
    path('recipes/add/', views.AddRecipeView.as_view(), name="add_recipe"),
    path('units/', views.UnitListView.as_view(), name="units"),
    path('units/add/', views.AddUnitView.as_view(), name="add_unit"),
    path('recipes/<int:pk>/edit/', views.EditRecipeView.as_view(), name="edit_recipe"),
    path('recipes/<int:pk>/delete/', views.DeleteRecipeView.as_view(), name="delete_recipe"),
    path('ingredients/<int:pk>/edit/', views.EditIngredientView.as_view(), name="edit_ingredient"),
    path('ingredients/<int:pk>/delete/', views.DeleteIngredientView.as_view(), name="delete_ingredient"),
    path('units/<int:pk>/edit/', views.EditUnitView.as_view(), name="edit_unit"),
    path('units/<int:pk>/delete/', views.DeleteUnitView.as_view(), name="delete_unit"),
    path('about/', views.AboutView.as_view(), name="about"),
]
