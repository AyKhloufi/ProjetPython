from django.views.generic.base import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Unit
from ..forms import UnitForm

# Read # 

class UnitListView(View):
    def get(self, request):
        units_list = Unit.objects.all()
        paginator = Paginator(units_list, 8)  # 8 unités par page (2 lignes de 4)
        
        page = request.GET.get('page')
        try:
            units = paginator.page(page)
        except PageNotAnInteger:
            units = paginator.page(1)
        except EmptyPage:
            units = paginator.page(paginator.num_pages)
            
        return render(request, 'App/unit/unit_list.html', {'units': units})

# Create #

class AddUnitView(View):
    def get(self, request):
        form = UnitForm()
        return render(request, 'App/unit/add_unit.html', {'form': form})

    def post(self, request):
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Unité ajoutée avec succès!')
            return redirect('units')
        return render(request, 'App/unit/add_unit.html', {'form': form})


# Update #

class EditUnitView(View):
    def get(self, request, pk):
        unit = get_object_or_404(Unit, pk=pk)
        form = UnitForm(instance=unit)
        return render(request, 'App/unit/edit_unit.html', {
            'unit': unit, 
            'form': form
        })

    def post(self, request, pk):
        unit = get_object_or_404(Unit, pk=pk)
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Unité modifiée avec succès!')
            return redirect('units')
        return render(request, 'App/unit/edit_unit.html', {
            'unit': unit, 
            'form': form
        })


# Delete #

class DeleteUnitView(View):
    def post(self, request, pk):
        unit = get_object_or_404(Unit, pk=pk)
        unit_name = unit.unit
        unit.delete()
        messages.success(request, f'Unité "{unit_name}" supprimée avec succès!')
        return redirect('units')