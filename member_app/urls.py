from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.UserCreationView.as_view(), name='user_create'),
    path('edit/', views.UserChangeView.as_view(), name='user_edit'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('password/', views.MyPasswordChangeView.as_view(), name="password_edit"),
    path('password-success/', views.PasswordChangeSuccessView.as_view(), name='password_edit_success'),
]
