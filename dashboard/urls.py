from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name='dashboard'
urlpatterns = [
    path('dashboard/', views.index, name="dashboard"),
    path('wallet/', views.billing, name='wallet'),
    path('profile/', views.profile, name='profile'),
    path('tables/', views.tables, name="tables"),
    path('vr/', views.virtual_reality, name='vr'),
    path('settings/' ,views.wallet_settings, name='ws'),

    # Authentication
    path('accounts/login/', views.login_user, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name="password_change_done"),
    path('accounts/password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', 
        views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
 ]




