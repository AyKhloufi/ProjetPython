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


class RecipeForm(forms.ModelForm):
    """Formulaire pour ajouter/modifier une recette (sans les ingrédients)"""
    
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'instructions', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'instructions': forms.Textarea(attrs={'rows': 6}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnalisation des champs
        self.fields['title'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Donnez un nom délicieux à votre recette...',
            'id': 'title'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Décrivez votre recette en quelques mots...',
            'id': 'description'
        })
        self.fields['instructions'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '1. Commencez par...\n2. Ensuite...\n3. Finalement...',
            'id': 'instructions'
        })
        self.fields['image'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'id': 'image'
        })
        
    def clean_title(self):
        """Validation personnalisée pour le titre"""
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError("Le titre de la recette est obligatoire.")
        return title
        
    def clean_description(self):
        """Validation personnalisée pour la description"""
        description = self.cleaned_data.get('description', '').strip()
        if not description:
            raise forms.ValidationError("La description est obligatoire.")
        return description
        
    def clean_instructions(self):
        """Validation personnalisée pour les instructions"""
        instructions = self.cleaned_data.get('instructions', '').strip()
        if not instructions:
            raise forms.ValidationError("Les instructions sont obligatoires.")
        return instructions


class RecipeIngredientForm(forms.ModelForm):
    """Formulaire pour gérer les ingrédients d'une recette"""
    
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity', 'unit']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnalisation des champs
        self.fields['ingredient'].widget.attrs.update({
            'class': 'form-select form-select-sm'
        })
        self.fields['quantity'].widget.attrs.update({
            'class': 'form-control form-control-sm',
            'min': '0.01',
            'step': 'any',
            'placeholder': '0.0'
        })
        self.fields['unit'].widget.attrs.update({
            'class': 'form-select form-select-sm'
        })
        
        # Définir les querysets pour optimiser les requêtes
        self.fields['ingredient'].queryset = Ingredient.objects.all().order_by('name')
        self.fields['unit'].queryset = Unit.objects.all().order_by('unit')


# Formset pour gérer plusieurs ingrédients dans une recette
RecipeIngredientFormSet = forms.inlineformset_factory(
    Recipe, 
    RecipeIngredient,
    form=RecipeIngredientForm,
    extra=0,  # Pas de formulaires vides par défaut
    can_delete=True,
    min_num=1,  # Au moins un ingrédient requis
    validate_min=True
)


class RecipeSearchForm(forms.Form):
    """Formulaire de recherche pour les recettes"""
    
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher une recette...',
            'id': 'search_query'
        })
    )
    
    ingredient = forms.ModelChoiceField(
        queryset=Ingredient.objects.all(),
        required=False,
        empty_label="Tous les ingrédients",
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'ingredient_filter'
        })
    )


class IngredientSearchForm(forms.Form):
    """Formulaire de recherche pour les ingrédients"""
    
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher un ingrédient...',
            'id': 'search_query'
        })
    )


class UnitSearchForm(forms.Form):
    """Formulaire de recherche pour les unités"""
    
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher une unité...',
            'id': 'search_query'
        })
    )
    
    unit_type = forms.ChoiceField(
        choices=[
            ('', 'Tous les types'),
            ('weight', 'Poids'),
            ('volume', 'Volume'),
            ('kitchen', 'Cuisine'),
            ('other', 'Autre')
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'unit_type_filter'
        })
    )
