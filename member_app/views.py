from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.views.generic.base import View

from .forms import MyAuthenticationForm, MyPasswordChangeForm, MyUserChangeForm, MyUserCreationForm


class MyLoginView(LoginView):
    form_class = MyAuthenticationForm
    template_name = 'member_app/login.html'
    success_url = reverse_lazy('index')


class MyLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("index")


class UserCreationView(CreateView):
    form_class = MyUserCreationForm
    template_name = 'member_app/user_create.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        # Sauvegarder l'utilisateur
        response = super().form_valid(form)
        
        # Ajouter l'utilisateur au groupe "Cuisinier"
        try:
            cuisinier_group = Group.objects.get(name='Cuisinier')
            self.object.groups.add(cuisinier_group)
        except Group.DoesNotExist:
            # Le groupe n'existe pas encore
            print("Le groupe 'Cuisinier' n'existe pas. Créez-le via l'admin Django.")
        
        return response


class UserChangeView(LoginRequiredMixin, UpdateView):
    form_class = MyUserChangeForm
    template_name = 'member_app/user_edit.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        return self.request.user


class MyPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = MyPasswordChangeForm
    template_name = 'member_app/password_edit.html'
    success_url = reverse_lazy('password_edit_success')


class PasswordChangeSuccessView(LoginRequiredMixin, View):
    template_name = "member_app/password_edit_success.html"

    def get(self, request):
        return render(request, self.template_name)
