from modeltranslation.translator import register, TranslationOptions
from .models import Recipe, Ingredient, Unit


@register(Recipe)
class RecipeTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'instructions')


@register(Ingredient)
class IngredientTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Unit)
class UnitTranslationOptions(TranslationOptions):
    fields = ('unit',)