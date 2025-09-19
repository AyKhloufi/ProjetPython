from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from .models import Recipe, Ingredient, Unit, RecipeIngredient

# Home #

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


# Read # 

class RecipeListView(View):
    def get(self, request):
        recipes = Recipe.objects.all()

        return render(request, 'recipes.html', {'recipes': recipes})
    
class IngredientListView(View):
    def get(self, request):
        ingredients = Ingredient.objects.all()
        return render(request, 'ingredient_list.html', {'ingredients': ingredients})


class UnitListView(View):
    def get(self, request):
        units = Unit.objects.all()
        return render(request, 'unit_list.html', {'units': units})

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

# Create #

class AddIngredientView(View):
    def get(self, request):
        return render(request, 'add_ingredient.html')

    def post(self, request):
        name = request.POST.get('name')
        if Ingredient.objects.filter(name__iexact=name).exists():
            return render(request, 'add_ingredient.html', {'message': "L'ingrédient existe déjà."})
        Ingredient.objects.create(name=name)
        return render(request, 'add_ingredient.html', {'message': 'Ingrédient ajouté avec succès!'})

class AddRecipeView(View):
    def get(self, request):
        ingredients = Ingredient.objects.all()
        units = Unit.objects.all()
        return render(request, 'add_recipe.html', {'ingredients': ingredients, 'units': units})

    def post(self, request):
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        instructions = request.POST.get('instructions', '').strip()

        # Validation des champs
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

        # Vérification des ingrédients sélectionnés
        ingredient_ids = request.POST.getlist('ingredient_ids')
        ingredients_data = []
        for ingredient_id in ingredient_ids:
            quantity = request.POST.get(f'quantity_{ingredient_id}')
            unit_id = request.POST.get(f'unit_{ingredient_id}')
            if not quantity or float(quantity) <= 0:
                ingredient = Ingredient.objects.filter(id=ingredient_id).first()
                errors.append(f"Une quantité valide est requise pour l'ingrédient {ingredient.name}.")
            if not unit_id:
                errors.append(f"Une unité est requise pour l'ingrédient {ingredient.name}.")
            ingredients_data.append((ingredient_id, quantity, unit_id))

        # Si erreurs, recharger le formulaire avec les données existantes
        if errors:
            ingredients = Ingredient.objects.all()
            units = Unit.objects.all()
            return render(request, 'add_recipe.html', {
                'errors': errors,
                'ingredients': ingredients,
                'units': units,
                'title': title,
                'description': description,
                'instructions': instructions,
            })

        # Création de la recette
        recipe = Recipe.objects.create(
            title=title, description=description, instructions=instructions
        )
        # Création des liaisons avec quantités et unités
        for ingredient_id, quantity, unit_id in ingredients_data:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id=ingredient_id,
                quantity=quantity,
                unit_id=unit_id
            )

        # Recharger le formulaire vide avec un message de succès
        ingredients = Ingredient.objects.all()
        units = Unit.objects.all()
        return render(request, 'add_recipe.html', {
            'message': 'Recette ajoutée avec succès!',
            'ingredients': ingredients,
            'units': units
        })

class AddUnitView(View):
    def get(self, request):
        return render(request, 'add_unit.html')

    def post(self, request):
        unit = request.POST.get('unit')
        if Unit.objects.filter(unit__iexact=unit).exists():
            return render(request, 'add_unit.html', {'message': "L'unité existe déjà."})
        Unit.objects.create(unit=unit)
        return render(request, 'add_unit.html', {'message': 'Unité ajoutée avec succès!'})



# Update #

class EditRecipeView(View):
    def get(self, request, pk):        
        recipe = get_object_or_404(Recipe, pk=pk)
        ingredients = Ingredient.objects.all()
        units = Unit.objects.all()
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

        # Validation des champs
        errors = []
        if not title:
            errors.append("Le titre de la recette est obligatoire.")
        if not description:
            errors.append("La description est obligatoire.")
        if not instructions:
            errors.append("Les instructions sont obligatoires.")
        if not ingredient_ids:
            errors.append("Veuillez sélectionner au moins un ingrédient.")

        # Vérification des ingrédients sélectionnés
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

        # Si erreurs, recharger le formulaire avec les données existantes
        if errors:
            ingredients = Ingredient.objects.all()
            units = Unit.objects.all()
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
        if Ingredient.objects.filter(name__iexact=name).exclude(pk=pk).exists():
            return render(request, 'edit_ingredient.html', {
                'ingredient': ingredient,
                'error': "Un autre ingrédient avec ce nom existe déjà."
            })
        ingredient.name = name
        ingredient.save()
        return redirect('ingredients')
    

class EditUnitView(View):
    def get(self, request, pk):
        unit = get_object_or_404(Unit, pk=pk)
        return render(request, 'edit_unit.html', {'unit': unit})

    def post(self, request, pk):
        unit = get_object_or_404(Unit, pk=pk)
        unit_name = request.POST.get('unit', '').strip()
        if not unit_name:
            return render(request, 'edit_unit.html', {
                'unit': unit,
                'error': "Le nom de l'unité ne peut pas être vide."
            })
        if Unit.objects.filter(unit__iexact=unit_name).exclude(pk=pk).exists():
            return render(request, 'edit_unit.html', {
                'unit': unit,
                'error': "Une autre unité avec ce nom existe déjà."
            })
        unit.unit = unit_name
        unit.save()
        return redirect('units')



# Delete #

class DeleteRecipeView(View):
    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        recipe.delete()
        return redirect('recipes')

    
class DeleteIngredientView(View):
    def post(self, request, pk):
        ingredient = get_object_or_404(Ingredient, pk=pk)
        ingredient.delete()
        return redirect('ingredients')


class DeleteUnitView(View):
    def post(self, request, pk):
        unit = get_object_or_404(Unit, pk=pk)
        unit.delete()
        return redirect('units')


# About #
class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')