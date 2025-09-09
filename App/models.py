from django.db import models

# Create your models here.

class Recipe(models.Model):
    title = models.CharField(max_length=100, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    ingredients = models.TextField(verbose_name="Ingredients")
    instructions = models.TextField(verbose_name="Instructions")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Crée le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")
    category = models.ForeignKey('Category', related_name='recipes', on_delete=models.CASCADE, verbose_name="Catégorie")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "recipe"
        verbose_name_plural = "recipes"


class Ingredient(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nom")
    quantity = models.CharField(max_length=50, verbose_name="Quantité")
    unit = models.CharField(max_length=20, verbose_name="Unité", blank=True, null=True)
    recipe = models.ForeignKey(Recipe, related_name='ingredients_list', on_delete=models.CASCADE, verbose_name="Recette")
    

    def __str__(self):
        return f"{self.quantity} of {self.name}"

    class Meta:
        ordering = ('name',)
        verbose_name = "ingredient"
        verbose_name_plural = "ingredients"

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nom")
    description = models.TextField(verbose_name="Description", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )
        verbose_name = "catégorie"
        verbose_name_plural = "catégories"

