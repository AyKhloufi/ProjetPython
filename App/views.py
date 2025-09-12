from django.http import Http404
from django.shortcuts import render
from django.views.generic.base import View
from .models import Recipe, Ingredient, QuantityUnit, RecipeIngredient



class IndexView(View):
    def get(self, request):
        recipes = Recipe.objects.all()

        return render(request, 'index.html', {'recipes': recipes})

class RecipeDetailView(View):
    def get(self, request, pk):
        recipe = Recipe.objects.get(pk=pk)
        if not recipe:
            raise Http404("Recipe not found")
        return render(request, 'recipe_detail.html', {'recipe': recipe})

class AddIngredientView(View):
    def get(self, request):
        quantity_units = QuantityUnit.objects.all()
        return render(request, 'add_ingredient.html', {'quantity_units': quantity_units})

    def post(self, request):
        name = request.POST.get('name')
        ingredient = Ingredient.objects.create(name=name)
        quantity_units = QuantityUnit.objects.all()
        return render(request, 'add_ingredient.html', {'message': 'Ingrédient ajouté avec succès!', 'quantity_units': quantity_units})

class AddRecipeView(View):
    def get(self, request):
        ingredients = Ingredient.objects.all()
        return render(request, 'add_recipe.html', {'ingredients': ingredients})

    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description')
        ingredients = request.POST.getlist('ingredients')
        recipe = Recipe.objects.create(title=title, description=description, created_at=None, updated_at=None)
        ingredients = Ingredient.objects.all()
        return render(request, 'add_recipe.html', {'message': 'Recette ajoutée avec succès!', 'ingredients': ingredients})

class IngredientListView(View):
    def get(self, request):
        ingredients = Ingredient.objects.all()
        return render(request, 'ingredient_list.html', {'ingredients': ingredients})

class IngredientDetailView(View):
    def get(self, request, pk):
        ingredient = Ingredient.objects.get(pk=pk)
        return render(request, 'ingredient_detail.html', {'ingredient': ingredient})

class QuantityUnitListView(View):
    def get(self, request):
        quantity_units = QuantityUnit.objects.all()
        return render(request, 'quantity_unit_list.html', {'quantity_units': quantity_units})

class AddQuantityUnitView(View):
    def get(self, request):
        return render(request, 'add_quantity_unit.html')

    def post(self, request):
        unit = request.POST.get('unit')
        QuantityUnit.objects.create(unit=unit)
        return render(request, 'add_quantity_unit.html', {'message': 'Unité de quantité ajoutée avec succès!'})

