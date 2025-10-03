from django.shortcuts import render, redirect, get_object_or_404
from ..models import Ingredient
from ..forms import IngredientForm
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
    permission_required = 'App.add_ingredient'

    def get(self, request):
        form = IngredientForm()
        return render(request, 'App/ingredient/add_ingredient.html', {'form': form})

    def post(self, request):
        form = IngredientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingrédient ajouté avec succès!')
            return redirect('ingredients')
        return render(request, 'App/ingredient/add_ingredient.html', {'form': form})

# Update #

class EditIngredientView(View):
    permission_required = 'App.change_ingredient'

    def get(self, request, pk):
        ingredient = get_object_or_404(Ingredient, pk=pk)
        form = IngredientForm(instance=ingredient)
        return render(request, 'App/ingredient/edit_ingredient.html', {
            'ingredient': ingredient, 
            'form': form
        })

    def post(self, request, pk):
        ingredient = get_object_or_404(Ingredient, pk=pk)
        form = IngredientForm(request.POST, request.FILES, instance=ingredient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingrédient modifié avec succès!')
            return redirect('ingredients')
        return render(request, 'App/ingredient/edit_ingredient.html', {
            'ingredient': ingredient, 
            'form': form
        })

# Delete #

class DeleteIngredientView(View):
    permission_required = 'App.delete_ingredient'

    def post(self, request, pk):
        ingredient = get_object_or_404(Ingredient, pk=pk)
        ingredient_name = ingredient.name
        ingredient.delete()
        messages.success(request, f'Ingrédient "{ingredient_name}" supprimé avec succès!')
        return redirect('ingredients')