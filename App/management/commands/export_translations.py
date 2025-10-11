from django.core.management.base import BaseCommand
import json
from App.models import Recipe, Ingredient, Unit

class Command(BaseCommand):
    help = 'Export all data that needs translation to JSON format'

    def handle(self, *args, **options):
        data_to_translate = {
            "ingredients": [],
            "units": [],
            "recipes": []
        }

        # Export ingredients (accès direct aux champs de base)
        for ingredient in Ingredient.objects.all():
            # Essayer d'accéder au champ original via la DB
            name_value = getattr(ingredient, 'name_fr_ca', None) or getattr(ingredient, 'name', None)
            data_to_translate["ingredients"].append({
                "id": ingredient.id,
                "name_fr": name_value or f"Ingrédient {ingredient.id}",
                "name_en": ""  # À traduire
            })

        # Export units
        for unit in Unit.objects.all():
            unit_value = getattr(unit, 'unit_fr_ca', None) or getattr(unit, 'unit', None)
            data_to_translate["units"].append({
                "id": unit.id,
                "unit_fr": unit_value or f"Unité {unit.id}",
                "unit_en": ""  # À traduire
            })

        # Export recipes
        for recipe in Recipe.objects.all():
            title_value = getattr(recipe, 'title_fr_ca', None) or getattr(recipe, 'title', None)
            desc_value = getattr(recipe, 'description_fr_ca', None) or getattr(recipe, 'description', None)
            instr_value = getattr(recipe, 'instructions_fr_ca', None) or getattr(recipe, 'instructions', None)
            
            data_to_translate["recipes"].append({
                "id": recipe.id,
                "title_fr": title_value or f"Recette {recipe.id}",
                "title_en": "",  # À traduire
                "description_fr": desc_value or "",
                "description_en": "",  # À traduire
                "instructions_fr": instr_value or "",
                "instructions_en": ""  # À traduire
            })

        # Print JSON format
        json_output = json.dumps(data_to_translate, indent=2, ensure_ascii=False)
        self.stdout.write(json_output)
        
        # Save to file
        with open('translation_data.json', 'w', encoding='utf-8') as f:
            f.write(json_output)
            
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Données exportées dans translation_data.json\n'
                f'📊 {len(data_to_translate["ingredients"])} ingrédients\n'
                f'📊 {len(data_to_translate["units"])} unités\n' 
                f'📊 {len(data_to_translate["recipes"])} recettes\n'
            )
        )