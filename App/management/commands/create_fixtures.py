from django.core.management.base import BaseCommand
from django.core import serializers
from App.models import Recipe, Ingredient, Unit, RecipeIngredient
import json

class Command(BaseCommand):
    help = 'Export current database data with translations to fixtures'

    def handle(self, *args, **options):
        
        # Créer les fixtures avec toutes les données traduites
        fixtures_data = []
        
        # Export des unités
        for unit in Unit.objects.all():
            fixtures_data.append({
                "model": "App.unit",
                "pk": unit.pk,
                "fields": {
                    "unit": getattr(unit, 'unit_fr_ca', unit.unit) or unit.unit,
                    "unit_fr_ca": getattr(unit, 'unit_fr_ca', unit.unit),
                    "unit_en": getattr(unit, 'unit_en', None)
                }
            })
        
        # Export des ingrédients
        for ingredient in Ingredient.objects.all():
            fixtures_data.append({
                "model": "App.ingredient",
                "pk": ingredient.pk,
                "fields": {
                    "name": getattr(ingredient, 'name_fr_ca', ingredient.name) or ingredient.name,
                    "name_fr_ca": getattr(ingredient, 'name_fr_ca', ingredient.name),
                    "name_en": getattr(ingredient, 'name_en', None),
                    "image": str(ingredient.image) if ingredient.image else ""
                }
            })
        
        # Export des recettes
        for recipe in Recipe.objects.all():
            user_id = recipe.user.pk if recipe.user else None
            fixtures_data.append({
                "model": "App.recipe",
                "pk": recipe.pk,
                "fields": {
                    "title": getattr(recipe, 'title_fr_ca', recipe.title) or recipe.title,
                    "title_fr_ca": getattr(recipe, 'title_fr_ca', recipe.title),
                    "title_en": getattr(recipe, 'title_en', None),
                    "description": getattr(recipe, 'description_fr_ca', recipe.description) or recipe.description,
                    "description_fr_ca": getattr(recipe, 'description_fr_ca', recipe.description),
                    "description_en": getattr(recipe, 'description_en', None),
                    "instructions": getattr(recipe, 'instructions_fr_ca', recipe.instructions) or recipe.instructions,
                    "instructions_fr_ca": getattr(recipe, 'instructions_fr_ca', recipe.instructions),
                    "instructions_en": getattr(recipe, 'instructions_en', None),
                    "created_at": recipe.created_at.isoformat() if recipe.created_at else None,
                    "updated_at": recipe.updated_at.isoformat() if recipe.updated_at else None,
                    "image": str(recipe.image) if recipe.image else "",
                    "user": user_id
                }
            })
        
        # Export des relations RecipeIngredient
        for ri in RecipeIngredient.objects.all():
            fixtures_data.append({
                "model": "App.recipeingredient", 
                "pk": ri.pk,
                "fields": {
                    "recipe": ri.recipe.pk,
                    "ingredient": ri.ingredient.pk,
                    "quantity": str(ri.quantity),
                    "unit": ri.unit.pk
                }
            })
        
        # Sauvegarder dans le fichier fixtures
        output_file = 'App/fixtures/complete_translated_data.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(fixtures_data, f, indent=2, ensure_ascii=False)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 FIXTURES GÉNÉRÉES AVEC SUCCÈS !\n'
                f'📁 Fichier: {output_file}\n'
                f'📊 {len([f for f in fixtures_data if f["model"] == "App.unit"])} unités\n'
                f'📊 {len([f for f in fixtures_data if f["model"] == "App.ingredient"])} ingrédients\n'
                f'📊 {len([f for f in fixtures_data if f["model"] == "App.recipe"])} recettes\n'
                f'📊 {len([f for f in fixtures_data if f["model"] == "App.recipeingredient"])} relations recette-ingrédient\n'
                f'\n💡 Pour restaurer: python manage.py loaddata complete_translated_data.json'
            )
        )