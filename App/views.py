from django.http import Http404
from django.shortcuts import render
from django.views.generic.base import View



class IndexView(View):
    def get(self, request):
        # fetch in
        recipes = [
            {"id": 1, "title": "Spaghetti Carbonara", "description": "A classic Italian pasta dish."},
            {"id": 2, "title": "Chicken Curry", "description": "A spicy and flavorful dish."},
        ]
        return render(request, 'index.html', {'recipes': recipes})
    
class RecipeDetailView(View):
    def get(self, request, pk):
        recipes = {
            1: {"title": "Spaghetti Carbonara", "description": "A classic Italian pasta dish."},
            2: {"title": "Chicken Curry", "description": "A spicy and flavorful dish."},
        }
        recipe = recipes.get(pk)
        if not recipe:
            raise Http404("Recipe not found")
        return render(request, 'recipe_detail.html', {'recipe': recipe})
