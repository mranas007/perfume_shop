from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('email-confirmation/', views.email_confirmation_alert, name='email-confirmation'),
    path('resend-activation-email/', views.resend_activation_email, name='resend-activation-email'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('logout/', views.logout_view, name='logout'),

    path('profile/', views.profile_view, name='profile'),
    path('update-profile/', views.update_profile_view, name='update_profile'),
    path('change-password/', views.change_password_view, name='change_password'),
]