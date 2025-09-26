from django.views.generic.base import View
from django.shortcuts import render, redirect, get_object_or_404
from ..models import Recipe, Ingredient, Unit, RecipeIngredient
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

        return render(request, 'App/recipe/recipes.html', {'recipes': recipes})
    
class RecipeDetailView(View):
    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe).select_related('ingredient', 'unit')
        return render(request, 'App/recipe/recipe_detail.html', {
            'recipe': recipe,
            'recipe_ingredients': recipe_ingredients,        })

# Create #

class AddRecipeView(View):
    def get(self, request):
        ingredients = Ingredient.objects.all()
        units = Unit.objects.all()
        return render(request, 'App/recipe/add_recipe.html', {'ingredients': ingredients, 'units': units})

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
            ingredients_data.append((ingredient_id, quantity, unit_id))        # Si erreurs, recharger le formulaire avec les données existantes
        if errors:
            ingredients = Ingredient.objects.all()
            units = Unit.objects.all()
            return render(request, 'App/recipe/add_recipe.html', {
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

# Update #

class EditRecipeView(View):
    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        ingredients = Ingredient.objects.all()
        units = Unit.objects.all()
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe).select_related('ingredient', 'unit')
        ri_dict = {ri.ingredient.id: ri for ri in recipe_ingredients}
        return render(request, 'App/recipe/edit_recipe.html', {
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
            return render(request, 'App/recipe/edit_recipe.html', {
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
    

# Delete #

class DeleteRecipeView(View):
    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        recipe_title = recipe.title
        recipe.delete()
        messages.success(request, f'Recette "{recipe_title}" supprimée avec succès!')
        return redirect('recipes')