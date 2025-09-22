from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Recipe, Ingredient, Unit, RecipeIngredient

# Home #

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


# Read # 

class RecipeListView(View):
    def get(self, request):
        recipes_list = Recipe.objects.all()
        paginator = Paginator(recipes_list, 6)  # 6 recettes par page (2 lignes de 3)
        
        page = request.GET.get('page')
        try:
            recipes = paginator.page(page)
        except PageNotAnInteger:
            recipes = paginator.page(1)
        except EmptyPage:
            recipes = paginator.page(paginator.num_pages)

        return render(request, 'recipes.html', {'recipes': recipes})
    
class IngredientListView(View):
    def get(self, request):
        ingredients_list = Ingredient.objects.all()
        paginator = Paginator(ingredients_list, 9)  # 9 ingrédients par page (3 lignes de 3)
        
        page = request.GET.get('page')
        try:
            ingredients = paginator.page(page)
        except PageNotAnInteger:
            ingredients = paginator.page(1)
        except EmptyPage:
            ingredients = paginator.page(paginator.num_pages)
            
        return render(request, 'ingredient_list.html', {'ingredients': ingredients})


class UnitListView(View):
    def get(self, request):
        units_list = Unit.objects.all()
        paginator = Paginator(units_list, 8)  # 8 unités par page (2 lignes de 4)
        
        page = request.GET.get('page')
        try:
            units = paginator.page(page)
        except PageNotAnInteger:
            units = paginator.page(1)
        except EmptyPage:
            units = paginator.page(paginator.num_pages)
            
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
        name = request.POST.get('name', '').strip()
        if not name:
            messages.error(request, "Le nom de l'ingrédient ne peut pas être vide.")
            return render(request, 'add_ingredient.html')
        if Ingredient.objects.filter(name__iexact=name).exists():
            messages.error(request, "L'ingrédient existe déjà.")
            return render(request, 'add_ingredient.html')
        Ingredient.objects.create(name=name)
        messages.success(request, 'Ingrédient ajouté avec succès!')
        return redirect('ingredients')

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

        messages.success(request, 'Recette ajoutée avec succès!')
        return redirect('recipes')

class AddUnitView(View):
    def get(self, request):
        return render(request, 'add_unit.html')

    def post(self, request):
        unit = request.POST.get('unit', '').strip()
        if not unit:
            messages.error(request, "Le nom de l'unité ne peut pas être vide.")
            return render(request, 'add_unit.html')
        if Unit.objects.filter(unit__iexact=unit).exists():
            messages.error(request, "L'unité existe déjà.")
            return render(request, 'add_unit.html')
        Unit.objects.create(unit=unit)
        messages.success(request, 'Unité ajoutée avec succès!')
        return redirect('units')



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

        messages.success(request, 'Recette modifiée avec succès!')
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
        messages.success(request, 'Ingrédient modifié avec succès!')
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
        messages.success(request, 'Unité modifiée avec succès!')
        return redirect('units')



# Delete #

class DeleteRecipeView(View):
    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        recipe_title = recipe.title
        recipe.delete()
        messages.success(request, f'Recette "{recipe_title}" supprimée avec succès!')
        return redirect('recipes')

    
class DeleteIngredientView(View):
    def post(self, request, pk):
        ingredient = get_object_or_404(Ingredient, pk=pk)
        ingredient_name = ingredient.name
        ingredient.delete()
        messages.success(request, f'Ingrédient "{ingredient_name}" supprimé avec succès!')
        return redirect('ingredients')


class DeleteUnitView(View):
    def post(self, request, pk):
        unit = get_object_or_404(Unit, pk=pk)
        unit_name = unit.unit
        unit.delete()
        messages.success(request, f'Unité "{unit_name}" supprimée avec succès!')
        return redirect('units')


# About #
class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')