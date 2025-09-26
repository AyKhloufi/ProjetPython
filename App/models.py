from django.db import models

# Create your models here.

class Recipe(models.Model):
    title = models.CharField(max_length=100, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    instructions = models.TextField(verbose_name="Instructions")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Crée le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")
    image = models.ImageField(default="", upload_to='recipes/', verbose_name="Image", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "recipe"
        verbose_name_plural = "recipes"

class Ingredient(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nom")
    image = models.ImageField(default="", upload_to='ingredients/', verbose_name="Image", blank=True, null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = "ingredient"
        verbose_name_plural = "ingredients"

class Unit(models.Model):
    unit = models.CharField(max_length=20, verbose_name="Unité")

    def __str__(self):
        return self.unit

    class Meta:
        ordering = ('unit',)
        verbose_name = "unité"
        verbose_name_plural = "unités"

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='recipe_ingredients', on_delete=models.CASCADE, verbose_name="Recette")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name="Ingrédient")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Quantité")
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name="Unité")

    def __str__(self):
        return f"{self.quantity} {self.unit} de {self.ingredient.name}"
    class Meta:
        unique_together = ('recipe', 'ingredient')
        verbose_name = "ingrédient de recette"
        verbose_name_plural = "ingrédients de recette"
    @property
    def quantity_str(self):
        # Convertit la quantité en string avec point décimal pour HTML input
        return str(self.quantity).replace(',', '.')
