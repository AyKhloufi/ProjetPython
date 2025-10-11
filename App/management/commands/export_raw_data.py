from django.core.management.base import BaseCommand
import json
from django.db import connection

class Command(BaseCommand):
    help = 'Export raw data from database for translation'

    def handle(self, *args, **options):
        data_to_translate = {
            "ingredients": [],
            "units": [],
            "recipes": []
        }

        with connection.cursor() as cursor:
            # Get ingredients
            cursor.execute("SELECT id, name FROM App_ingredient")
            for row in cursor.fetchall():
                data_to_translate["ingredients"].append({
                    "id": row[0],
                    "name_fr": row[1] or f"Ingrédient {row[0]}",
                    "name_en": ""
                })

            # Get units  
            cursor.execute("SELECT id, unit FROM App_unit")
            for row in cursor.fetchall():
                data_to_translate["units"].append({
                    "id": row[0],
                    "unit_fr": row[1] or f"Unité {row[0]}",
                    "unit_en": ""
                })

            # Get recipes
            cursor.execute("SELECT id, title, description, instructions FROM App_recipe")
            for row in cursor.fetchall():
                data_to_translate["recipes"].append({
                    "id": row[0],
                    "title_fr": row[1] or f"Recette {row[0]}",
                    "title_en": "",
                    "description_fr": row[2] or "",
                    "description_en": "",
                    "instructions_fr": row[3] or "",
                    "instructions_en": ""
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