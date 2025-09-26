from django.shortcuts import render, redirect, get_object_or_404
from ..models import Ingredient
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

# Read # 

class IngredientListView(View):
    def get(self, request):
        ingredients_list = Ingredient.objects.all()
        paginator = Paginator(ingredients_list, 9)  # 9 ingrédients par page (3 lignes de 3)
        
        page = request.GET.get('page')
        try:
            ingredients = paginator.page(page)
        except PageNotAnInteger:
            ingredients = paginator.page(1)
        except EmptyPage:
            ingredients = paginator.page(paginator.num_pages)
            
        return render(request, 'App/ingredient/ingredient_list.html', {'ingredients': ingredients})



# Create #

class AddIngredientView(View):
    def get(self, request):
        return render(request, 'App/ingredient/add_ingredient.html')

    def post(self, request):
        name = request.POST.get('name', '').strip()
        if not name:
            messages.error(request, "Le nom de l'ingrédient ne peut pas être vide.")
            return render(request, 'App/ingredient/add_ingredient.html')
        if Ingredient.objects.filter(name__iexact=name).exists():
            messages.error(request, "L'ingrédient existe déjà.")
            return render(request, 'App/ingredient/add_ingredient.html')
        Ingredient.objects.create(name=name)
        messages.success(request, 'Ingrédient ajouté avec succès!')
        return redirect('ingredients')

# Update #

class EditIngredientView(View):
    def get(self, request, pk):
        ingredient = get_object_or_404(Ingredient, pk=pk)
        return render(request, 'App/ingredient/edit_ingredient.html', {'ingredient': ingredient})

    def post(self, request, pk):
        ingredient = get_object_or_404(Ingredient, pk=pk)
        name = request.POST.get('name', '').strip()
        if not name:
            return render(request, 'App/ingredient/edit_ingredient.html', {
                'ingredient': ingredient,
                'error': "Le nom de l'ingrédient ne peut pas être vide."
            })
        if Ingredient.objects.filter(name__iexact=name).exclude(pk=pk).exists():
            return render(request, 'App/ingredient/edit_ingredient.html', {
                'ingredient': ingredient,
                'error': "Un autre ingrédient avec ce nom existe déjà."
            })
        ingredient.name = name
        ingredient.save()
        messages.success(request, 'Ingrédient modifié avec succès!')
        return redirect('ingredients')

# Delete #

class DeleteIngredientView(View):
    def post(self, request, pk):
        ingredient = get_object_or_404(Ingredient, pk=pk)
        ingredient_name = ingredient.name
        ingredient.delete()
        messages.success(request, f'Ingrédient "{ingredient_name}" supprimé avec succès!')
        return redirect('ingredients')