from django.core.management.base import BaseCommand
import json
from App.models import Recipe, Ingredient, Unit
from django.db import transaction

class Command(BaseCommand):
    help = 'Import translations from JSON file into database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='translations_complete.json',
            help='JSON file containing translations'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        
        # Les données traduites complètes
        translations_data = {
            "ingredients": [
                {"id": 1, "name_fr": "Farine", "name_en": "Flour"},
                {"id": 2, "name_fr": "Sucre", "name_en": "Sugar"},
                {"id": 3, "name_fr": "Oeuf", "name_en": "Egg"},
                {"id": 4, "name_fr": "Lait", "name_en": "Milk"},
                {"id": 5, "name_fr": "Beurre", "name_en": "Butter"},
                {"id": 6, "name_fr": "Chocolat", "name_en": "Chocolate"},
                {"id": 7, "name_fr": "Levure", "name_en": "Yeast"},
                {"id": 8, "name_fr": "Sel", "name_en": "Salt"},
                {"id": 9, "name_fr": "Bananes", "name_en": "Bananas"},
                {"id": 10, "name_fr": "Pomme", "name_en": "Apple"},
                {"id": 11, "name_fr": "Fraise", "name_en": "Strawberry"},
                {"id": 13, "name_fr": "Pâte à pizza", "name_en": "Pizza dough"},
                {"id": 14, "name_fr": "Crème de cuisson 32%", "name_en": "Cooking cream 32%"},
                {"id": 15, "name_fr": "Poivrons", "name_en": "Bell peppers"},
                {"id": 16, "name_fr": "Olives", "name_en": "Olives"},
                {"id": 17, "name_fr": "Sauce fromagère (recette secrète)", "name_en": "Cheese sauce (secret recipe)"},
                {"id": 18, "name_fr": "Poivre", "name_en": "Pepper"},
                {"id": 19, "name_fr": "Poulet", "name_en": "Chicken"},
                {"id": 20, "name_fr": "Piment de cayenne", "name_en": "Cayenne pepper"},
                {"id": 21, "name_fr": "Mozzarella rapée", "name_en": "Shredded mozzarella"}
            ],
            "units": [
                {"id": 1, "unit_fr": "g", "unit_en": "g"},
                {"id": 2, "unit_fr": "ml", "unit_en": "ml"},
                {"id": 3, "unit_fr": "pièce", "unit_en": "piece"},
                {"id": 4, "unit_fr": "c. à soupe", "unit_en": "tbsp"},
                {"id": 5, "unit_fr": "c. à café", "unit_en": "tsp"}
            ],
            "recipes": [
                {
                    "id": 1,
                    "title_fr": "Crêpes",
                    "title_en": "Pancakes",
                    "description_fr": "Délicieuses crêpes maison",
                    "description_en": "Delicious homemade pancakes",
                    "instructions_fr": "1. Mélanger les ingrédients.\r\n2. Cuire à la poêle.",
                    "instructions_en": "1. Mix the ingredients.\r\n2. Cook in a pan."
                },
                {
                    "id": 2,
                    "title_fr": "Gâteau au chocolat",
                    "title_en": "Chocolate cake",
                    "description_fr": "Un gâteau moelleux au chocolat",
                    "description_en": "A soft chocolate cake",
                    "instructions_fr": "1. Faire fondre le chocolat et le beurre. 2. Mélanger avec les autres ingrédients. 3. Cuire au four.",
                    "instructions_en": "1. Melt the chocolate and butter. 2. Mix with other ingredients. 3. Bake in the oven."
                },
                {
                    "id": 3,
                    "title_fr": "Pancakes à la banane",
                    "title_en": "Banana pancakes",
                    "description_fr": "Pancakes moelleux à la banane",
                    "description_en": "Soft banana pancakes",
                    "instructions_fr": "1. Écraser les bananes. 2. Mélanger avec les autres ingrédients. 3. Cuire à la poêle.",
                    "instructions_en": "1. Mash the bananas. 2. Mix with other ingredients. 3. Cook in a pan."
                },
                {
                    "id": 4,
                    "title_fr": "Compote de pommes",
                    "title_en": "Apple compote",
                    "description_fr": "Compote maison sans sucre ajouté",
                    "description_en": "Homemade compote without added sugar",
                    "instructions_fr": "1. Éplucher et couper les pommes. 2. Cuire à feu doux avec un peu d eau.",
                    "instructions_en": "1. Peel and cut the apples. 2. Cook over low heat with a little water."
                },
                {
                    "id": 5,
                    "title_fr": "Muffins",
                    "title_en": "Muffins",
                    "description_fr": "Muffins moelleux pour le goûter",
                    "description_en": "Soft muffins for snack time",
                    "instructions_fr": "1. Mélanger les ingrédients secs. 2. Ajouter les ingrédients liquides. 3. Cuire au four.",
                    "instructions_en": "1. Mix dry ingredients. 2. Add liquid ingredients. 3. Bake in the oven."
                },
                {
                    "id": 7,
                    "title_fr": "Pizza boisée (à la lyonnaise)",
                    "title_en": "Woodland pizza (Lyon style)",
                    "description_fr": "Entre street-food lyonnaise et haute gastronomie, une saveur unique, un goût intense ...",
                    "description_en": "Between Lyon street-food and haute cuisine, a unique flavor, an intense taste...",
                    "instructions_fr": "1. Coupez poivrons en petites lamelles\r\n2. Faire revenir ses poivrons à la poêle avec un filet d'huile. Pendant ce temps, assaisonnez le poulet avec sel, poivre et piment de cayenne\r\n3. Retirez les poivrons de la poêle et cuire le poulet\r\n4. Préchauffez le four à 450°F\r\n5. Etalez la pizza puis y ajouter la crème, le poulet, les poivrons, les olives, et la mozzarella rappée\r\n6. Mettre au four pendant 15-20 min en fonction de la cuisson désirée\r\n7. Sortir la pizza après cuisson puis y ajouter la sauce fromagère en formant des cercles en partant du centre jusqu'à l'extrémité. \r\n8. Dégustez, bon voyage gustatif pour Lyon...",
                    "instructions_en": "1. Cut bell peppers into small strips\r\n2. Sauté the peppers in a pan with a drizzle of oil. Meanwhile, season the chicken with salt, pepper and cayenne pepper\r\n3. Remove peppers from pan and cook the chicken\r\n4. Preheat oven to 450°F\r\n5. Spread the pizza then add cream, chicken, peppers, olives, and shredded mozzarella\r\n6. Bake for 15-20 min depending on desired cooking\r\n7. Remove pizza after cooking then add cheese sauce forming circles from center to edge\r\n8. Enjoy, bon voyage to Lyon..."
                }
            ]
        }

        try:
            with transaction.atomic():
                # Import ingredients
                ingredients_updated = 0
                for item in translations_data["ingredients"]:
                    try:
                        ingredient = Ingredient.objects.get(id=item["id"])
                        ingredient.name_fr_ca = item["name_fr"]
                        ingredient.name_en = item["name_en"]
                        ingredient.save()
                        ingredients_updated += 1
                        self.stdout.write(f"✅ Ingrédient {item['id']}: {item['name_fr']} → {item['name_en']}")
                    except Ingredient.DoesNotExist:
                        self.stdout.write(f"⚠️  Ingrédient ID {item['id']} non trouvé")

                # Import units
                units_updated = 0
                for item in translations_data["units"]:
                    try:
                        unit = Unit.objects.get(id=item["id"])
                        unit.unit_fr_ca = item["unit_fr"]
                        unit.unit_en = item["unit_en"]
                        unit.save()
                        units_updated += 1
                        self.stdout.write(f"✅ Unité {item['id']}: {item['unit_fr']} → {item['unit_en']}")
                    except Unit.DoesNotExist:
                        self.stdout.write(f"⚠️  Unité ID {item['id']} non trouvée")

                # Import recipes
                recipes_updated = 0
                for item in translations_data["recipes"]:
                    try:
                        recipe = Recipe.objects.get(id=item["id"])
                        recipe.title_fr_ca = item["title_fr"]
                        recipe.title_en = item["title_en"]
                        recipe.description_fr_ca = item["description_fr"]
                        recipe.description_en = item["description_en"]
                        recipe.instructions_fr_ca = item["instructions_fr"]
                        recipe.instructions_en = item["instructions_en"]
                        recipe.save()
                        recipes_updated += 1
                        self.stdout.write(f"✅ Recette {item['id']}: {item['title_fr']} → {item['title_en']}")
                    except Recipe.DoesNotExist:
                        self.stdout.write(f"⚠️  Recette ID {item['id']} non trouvée")

                self.stdout.write(
                    self.style.SUCCESS(
                        f'\n🎉 IMPORT TERMINÉ AVEC SUCCÈS !\n'
                        f'📊 {ingredients_updated} ingrédients traduits\n'
                        f'📊 {units_updated} unités traduites\n' 
                        f'📊 {recipes_updated} recettes traduites\n'
                        f'\n🌐 Votre application est maintenant bilingue !'
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erreur lors de l\'import: {str(e)}')
            )