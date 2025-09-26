from django.views.generic.base import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Unit

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
        return render(request, 'App/unit/add_unit.html')

    def post(self, request):
        unit = request.POST.get('unit', '').strip()
        if not unit:
            messages.error(request, "Le nom de l'unité ne peut pas être vide.")
            return render(request, 'App/unit/add_unit.html')
        if Unit.objects.filter(unit__iexact=unit).exists():
            messages.error(request, "L'unité existe déjà.")
            return render(request, 'App/unit/add_unit.html')
        Unit.objects.create(unit=unit)
        messages.success(request, 'Unité ajoutée avec succès!')
        return redirect('units')


# Update #

class EditUnitView(View):
    def get(self, request, pk):
        unit = get_object_or_404(Unit, pk=pk)
        return render(request, 'App/unit/edit_unit.html', {'unit': unit})

    def post(self, request, pk):
        unit = get_object_or_404(Unit, pk=pk)
        unit_name = request.POST.get('unit', '').strip()
        if not unit_name:
            return render(request, 'App/unit/edit_unit.html', {
                'unit': unit,
                'error': "Le nom de l'unité ne peut pas être vide."
            })
        if Unit.objects.filter(unit__iexact=unit_name).exclude(pk=pk).exists():
            return render(request, 'App/unit/edit_unit.html', {
                'unit': unit,
                'error': "Une autre unité avec ce nom existe déjà."
            })
        unit.unit = unit_name
        unit.save()
        messages.success(request, 'Unité modifiée avec succès!')
        return redirect('units')


# Delete #

class DeleteUnitView(View):
    def post(self, request, pk):
        unit = get_object_or_404(Unit, pk=pk)
        unit_name = unit.unit
        unit.delete()
        messages.success(request, f'Unité "{unit_name}" supprimée avec succès!')
        return redirect('units')