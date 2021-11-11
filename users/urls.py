from users.forms import EmailValidationOnForgotPassword
from django.conf.urls import include, url
from django.urls import path
from django.urls.conf import re_path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),

    path('', views.profiles, name="profiles"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('account/', views.userAccount, name="account"),
    path('edit-account/', views.edit_account, name="edit-account"),

    path('verify_account/<auth_token>', views.verify_account, name="verify_account"),
    path('activation_request/', views.activation_request, name="activation_request"),
    path('activation_success/', views.activation_success, name="activation_success"),
    
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="users/reset_password.html"),
     name="reset_password"),
    path('reset_password_sent/',
     auth_views.PasswordResetDoneView.as_view(template_name="users/reset_password_sent.html"),
     name="password_reset_done"),
    path('reset/<uidb64>/<token>/', 
     auth_views.PasswordResetConfirmView.as_view(template_name="users/reset.html"),
     name="password_reset_confirm"),
    path('reset_password_complete/',
     auth_views.PasswordResetCompleteView.as_view(template_name="users/reset_password_complete.html"),
     name="password_reset_complete"),
    
    path('psreset/', views.psreset, name="psreset"),
    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=EmailValidationOnForgotPassword), name='password_reset'),
     
]