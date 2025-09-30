from django.contrib import admin
from django.utils.html import format_html
from .models import Recipe, Ingredient, Unit, RecipeIngredient

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    autocomplete_fields = ['ingredient', 'unit']

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'display_image', 'created_at', 'updated_at', 'display_ingredients_count']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'description', 'instructions']
    readonly_fields = ['created_at', 'updated_at', 'display_image']
    fieldsets = [
        ('Informations principales', {
            'fields': ['title', 'description', 'instructions', 'image', 'display_image']
        }),
        ('Métadonnées', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]
    inlines = [RecipeIngredientInline]

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "Aucune image"
    display_image.short_description = 'Aperçu'

    def display_ingredients_count(self, obj):
        return obj.recipe_ingredients.count()
    display_ingredients_count.short_description = 'Nombre d\'ingrédients'

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_image', 'display_recipes_count']
    search_fields = ['name']
    readonly_fields = ['display_image']
    ordering = ['name']

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "Aucune image"
    display_image.short_description = 'Aperçu'

    def display_recipes_count(self, obj):
        return obj.recipeingredient_set.count()
    display_recipes_count.short_description = 'Utilisé dans # recettes'

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['unit', 'display_usage_count']
    search_fields = ['unit']
    ordering = ['unit']

    def display_usage_count(self, obj):
        return obj.recipeingredient_set.count()
    display_usage_count.short_description = 'Utilisations'