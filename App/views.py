from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from .models import Recipe, Ingredient, QuantityUnit, RecipeIngredient

class IndexView(View):
    def get(self, request):
        recipes = Recipe.objects.all()

        return render(request, 'index.html', {'recipes': recipes})

class RecipeDetailView(View):
    def get(self, request, pk):
        try:
            recipe = Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            raise Http404("Recipe not found")
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe).select_related('ingredient', 'unit')
        return render(request, 'recipe_detail.html', {
            'recipe': recipe,
            'recipe_ingredients': recipe_ingredients,
        })


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
        units = QuantityUnit.objects.all()
        return render(request, 'add_recipe.html', {'ingredients': ingredients, 'units': units})

    def post(self, request):
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        instructions = request.POST.get('instructions', '').strip()

        errors = []
        if not title:
            errors.append("Le titre de la recette est obligatoire.")
        if not description:
            errors.append("La description est obligatoire.")
        if not instructions:
            errors.append("Les instructions sont obligatoires.")

        ingredient_ids = request.POST.getlist('ingredient_ids')
        if not ingredient_ids:
            errors.append("Veuillez sélectionner au moins un ingrédient.")


        ingredient_ids = request.POST.getlist('ingredient_ids')
        ingredients_data = []
        for ingredient_id in ingredient_ids:
            quantity = request.POST.get(f'quantity_{ingredient_id}')
            unit_id = request.POST.get(f'unit_{ingredient_id}')
            if not quantity or float(quantity) <= 0:
                errors.append(f"Une quantité valide est requise pour l'ingrédient {ingredient_id}.")
            if not unit_id:
                errors.append(f"Une unité est requise pour l'ingrédient {ingredient_id}.")
            ingredients_data.append((ingredient_id, quantity, unit_id))

        if errors:
            ingredients = Ingredient.objects.all()
            units = QuantityUnit.objects.all()
            return render(request, 'add_recipe.html', {
                'errors': errors,
                'ingredients': ingredients,
                'units': units,
                'title': title,
                'description': description,
                'instructions': instructions,
            })

        recipe = Recipe.objects.create(
            title=title, description=description, instructions=instructions
        )
        for ingredient_id, quantity, unit_id in ingredients_data:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id=ingredient_id,
                quantity=quantity,
                unit_id=unit_id
            )

        ingredients = Ingredient.objects.all()
        units = QuantityUnit.objects.all()
        return render(request, 'add_recipe.html', {
            'message': 'Recette ajoutée avec succès!',
            'ingredients': ingredients,
            'units': units
        })



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


class EditRecipeView(View):
    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        ingredients = Ingredient.objects.all()
        units = QuantityUnit.objects.all()
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe).select_related('ingredient', 'unit')
        ri_dict = {ri.ingredient.id: ri for ri in recipe_ingredients}
        return render(request, 'edit_recipe.html', {
            'recipe': recipe,
            'ingredients': ingredients,
            'units': units,
            'ri_dict': ri_dict,
        })

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        instructions = request.POST.get('instructions', '').strip()
        ingredient_ids = request.POST.getlist('ingredient_ids')

        errors = []
        if not title:
            errors.append("Le titre de la recette est obligatoire.")
        if not description:
            errors.append("La description est obligatoire.")
        if not instructions:
            errors.append("Les instructions sont obligatoires.")
        if not ingredient_ids:
            errors.append("Veuillez sélectionner au moins un ingrédient.")

        ingredients_data = []
        for iid in ingredient_ids:
            quantity = request.POST.get(f'quantity_{iid}')
            unit_id = request.POST.get(f'unit_{iid}')
            try:
                quantity_val = float(quantity)
                if quantity_val <= 0:
                    ingredient = Ingredient.objects.filter(id=iid).first()
                    errors.append(f"Quantité invalide pour l'ingrédient {ingredient.name}.")
            except (TypeError, ValueError):
                ingredient = Ingredient.objects.filter(id=iid).first()
                errors.append(f"Quantité invalide pour l'ingrédient {ingredient.name}.")
            if not unit_id:
                ingredient = Ingredient.objects.filter(id=iid).first()
                errors.append(f"Unité manquante pour l'ingrédient {ingredient.name}.")
            ingredients_data.append((iid, quantity, unit_id))

        if errors:
            ingredients = Ingredient.objects.all()
            units = QuantityUnit.objects.all()
            recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe).select_related('ingredient', 'unit')
            ri_dict = {ri.ingredient.id: ri for ri in recipe_ingredients}
            return render(request, 'edit_recipe.html', {
                'recipe': recipe,
                'ingredients': ingredients,
                'units': units,
                'ri_dict': ri_dict,
                'errors': errors,
                'title': title,
                'description': description,
                'instructions': instructions,
            })

        # Mise à jour de la recette
        recipe.title = title
        recipe.description = description
        recipe.instructions = instructions
        recipe.save()

        # Supprimer les anciennes liaisons ingrédients
        RecipeIngredient.objects.filter(recipe=recipe).delete()

        # Créer les nouvelles liaisons avec quantités et unités
        for iid, quantity, unit_id in ingredients_data:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id=iid,
                quantity=quantity,
                unit_id=unit_id
            )

        return redirect('recipe_detail', pk=recipe.pk)
    

class DeleteRecipeView(View):
    def post(self, request, pk):
        try:
            recipe = Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            raise Http404("Recipe not found")
        recipe.delete()
        return redirect('index')

    
class EditIngredientView(View):
    def get(self, request, pk):
        ingredient = get_object_or_404(Ingredient, pk=pk)
        return render(request, 'edit_ingredient.html', {'ingredient': ingredient})

    def post(self, request, pk):
        ingredient = get_object_or_404(Ingredient, pk=pk)
        name = request.POST.get('name', '').strip()
        if not name:
            return render(request, 'edit_ingredient.html', {
                'ingredient': ingredient,
                'error': "Le nom de l'ingrédient ne peut pas être vide."
            })
        ingredient.name = name
        ingredient.save()
        return redirect('ingredients')
    
class DeleteIngredientView(View):
    def post(self, request, pk):
        try:
            ingredient = Ingredient.objects.get(pk=pk)
        except Ingredient.DoesNotExist:
            raise Http404("Ingredient not found")
        ingredient.delete()
        return redirect('ingredients')
    
class EditQuantityUnitView(View):
    def get(self, request, pk):
        quantity_unit = get_object_or_404(QuantityUnit, pk=pk)
        return render(request, 'edit_quantity_unit.html', {'quantity_unit': quantity_unit})

    def post(self, request, pk):
        quantity_unit = get_object_or_404(QuantityUnit, pk=pk)
        unit = request.POST.get('unit', '').strip()
        if not unit:
            return render(request, 'edit_quantity_unit.html', {
                'quantity_unit': quantity_unit,
                'error': "Le nom de l'unité ne peut pas être vide."
            })
        quantity_unit.unit = unit
        quantity_unit.save()
        return redirect('quantity_units')

class DeleteQuantityUnitView(View):
    def post(self, request, pk):
        try:
            quantity_unit = QuantityUnit.objects.get(pk=pk)
        except QuantityUnit.DoesNotExist:
            raise Http404("Quantity Unit not found")
        quantity_unit.delete()
        return redirect('quantity_units')
    
    