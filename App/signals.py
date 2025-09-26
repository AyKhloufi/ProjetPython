from django.db.models.signals import post_delete, pre_save
from django.dispatch.dispatcher import receiver

from .models import Recipe, Ingredient


@receiver(post_delete, sender=Recipe)
def recipe_post_delete(sender, instance, **kwargs):
    # Permet de supprimer l'image de la recette sur le disque.
    instance.image.delete(False) # Passez False pour ne pas enregistrer le modèle.

@receiver(pre_save, sender=Recipe)
def recipe_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_image = sender.objects.get(pk=instance.pk).image
            if old_image != instance.image:
                # Permet de supprimer l'ancienne image de la recette sur le disque si modifiée.
                old_image.delete(False) # Passez False pour ne pas enregistrer le modèle.
        except Recipe.DoesNotExist:
            pass

@receiver(post_delete, sender=Ingredient)
def ingredient_post_delete(sender, instance, **kwargs):
    # Permet de supprimer l'image de l'ingrédient sur le disque.
    instance.image.delete(False) # Passez False pour ne pas enregistrer le modèle.
    
@receiver(pre_save, sender=Ingredient)
def ingredient_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_image = sender.objects.get(pk=instance.pk).image
            if old_image != instance.image:
                # Permet de supprimer l'ancienne image de l'ingrédient sur le disque si modifiée.
                old_image.delete(False) # Passez False pour ne pas enregistrer le modèle.
        except Ingredient.DoesNotExist:
            pass