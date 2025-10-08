from django import forms
from .models import Recipe, Ingredient, Unit, RecipeIngredient


class IngredientForm(forms.ModelForm):
    """Formulaire pour ajouter/modifier un ingrédient"""
    
    class Meta:
        model = Ingredient
        fields = ['name', 'image']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnalisation des champs
        self.fields['name'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Ex: Tomates, Fromage, Basilic...',
            'id': 'name'
        })
        self.fields['image'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'id': 'image'
        })
        
    def clean_name(self):
        """Validation personnalisée pour le nom"""
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise forms.ValidationError("Le nom de l'ingrédient ne peut pas être vide.")
        
        # Vérifier l'unicité (exclure l'instance courante en cas de modification)
        queryset = Ingredient.objects.filter(name__iexact=name)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise forms.ValidationError("Un ingrédient avec ce nom existe déjà.")
        
        return name


class UnitForm(forms.ModelForm):
    """Formulaire pour ajouter/modifier une unité de mesure"""
    
    class Meta:
        model = Unit
        fields = ['unit']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnalisation des champs
        self.fields['unit'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Ex: g, ml, tasse, cuillère à soupe...',
            'id': 'unit'
        })
        
    def clean_unit(self):
        """Validation personnalisée pour l'unité"""
        unit = self.cleaned_data.get('unit', '').strip()
        if not unit:
            raise forms.ValidationError("L'unité ne peut pas être vide.")
        
        # Vérifier l'unicité (exclure l'instance courante en cas de modification)
        queryset = Unit.objects.filter(unit__iexact=unit)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise forms.ValidationError("Une unité avec ce nom existe déjà.")
        
        return unit









