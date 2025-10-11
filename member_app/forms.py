from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext_lazy as _


class MyAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        super(MyAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].label = _("Nom d'utilisateur")
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].label = _("Mot de passe")


class MyPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

    def __init__(self, *args, **kwargs):
        super(MyPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['old_password'].label = _("Ancien mot de passe")
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].label = _("Nouveau mot de passe")
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].label = _("Confirmation du nouveau mot de passe")


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined')

    def __init__(self, *args, **kwargs):
        super(MyUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].label = _("Nom d'utilisateur")
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].label = _("Prénom")
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].label = _("Nom de famille")
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].label = _("Adresse e-mail")
        self.fields['password'].widget = forms.HiddenInput()
        self.fields['last_login'].widget = forms.HiddenInput()
        self.fields['is_superuser'].widget = forms.HiddenInput()
        self.fields['is_staff'].widget = forms.HiddenInput()
        self.fields['is_active'].widget = forms.HiddenInput()
        self.fields['date_joined'].widget = forms.HiddenInput()


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].label = _("Nom d'utilisateur")
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].label = _("Prénom")
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].label = _("Nom de famille")
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].label = _("Adresse e-mail")
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].label = _("Mot de passe")
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].label = _("Confirmation du mot de passe")
