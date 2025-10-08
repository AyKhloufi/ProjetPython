from django import template
import re
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def format_instructions(text):
    """
    Formate les instructions de recette en convertissant les numéros en liste HTML
    Exemple: "1. Étape un 2. Étape deux" devient une liste HTML numérotée
    """
    if not text:
        return ""
    
    # Remplacer les retours à la ligne par des espaces pour une meilleure détection
    text = text.replace('\n', ' ').replace('\r', ' ')
    
    # Rechercher les patterns comme "1.", "2.", etc. suivi de texte
    pattern = r'(\d+\.\s*)'
    
    # Diviser le texte par les numéros
    parts = re.split(pattern, text)
    
    # Construire la liste HTML
    if len(parts) > 1:
        html_parts = ['<ol class="instruction-list">']
        
        # Traiter les parties (les indices impairs contiennent les numéros, les pairs le texte)
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                instruction_text = parts[i + 1].strip()
                if instruction_text:
                    html_parts.append(f'<li class="instruction-item">{instruction_text}</li>')
        
        html_parts.append('</ol>')
        return mark_safe(''.join(html_parts))
    
    # Si pas de numérotation trouvée, retourner le texte dans un paragraphe
    return mark_safe(f'<p class="instruction-text">{text}</p>')

@register.simple_tag
def can_edit_recipe(user, recipe):
    """Template tag pour vérifier si l'utilisateur peut modifier cette recette"""
    # Les gestionnaires peuvent tout faire
    if user.groups.filter(name='Gestionnaire').exists():
        return True
    # Les cuisiniers ne peuvent agir que sur leurs propres recettes
    if user.groups.filter(name='Cuisinier').exists():
        return recipe.user == user
    # Fallback: vérifier la permission générale
    return user.has_perm('App.change_recipe')

@register.simple_tag
def can_delete_recipe(user, recipe):
    """Template tag pour vérifier si l'utilisateur peut supprimer cette recette"""
    # Les gestionnaires peuvent tout faire
    if user.groups.filter(name='Gestionnaire').exists():
        return True
    # Les cuisiniers ne peuvent agir que sur leurs propres recettes
    if user.groups.filter(name='Cuisinier').exists():
        return recipe.user == user
    # Fallback: vérifier la permission générale
    return user.has_perm('App.delete_recipe')