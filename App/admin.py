from django.contrib import admin
from .models import Recipe, Ingredient, QuantityUnit, RecipeIngredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name',]
    search_fields = ['name']

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title',]
    search_fields = ['title', 'description']