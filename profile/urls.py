from django.contrib.auth import views
from django.urls import path, reverse_lazy
from .views import *
from django.contrib.auth import views
from servers.views import create_server
from profile.forms import UserLoginForm

app_name = 'account'

urlpatterns = [
    path('', account, name='main'),
    path('auth/', login, name='auth'),
    path('signup/', register, name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('server/<pk>/edit/', edit_server, name='edit'),
    path('server/<pk>/delete/', delete_server, name='delete'),
    path('status-server/', status_server, name='status'),
    path('create-server/', create_server, name='create'),
    path('change-username/', change_username, name='change-username'),
    path('password-recovery/', PasswordResetCustom.as_view(success_url=reverse_lazy('account:password_recovery_done')), name='password_recovery'),
    path('password-recovery/done/', views.PasswordResetDoneView.as_view(), name='password_recovery_done'),
    path('recovery/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('account:password_recovery_complete')), name='password_recovery_confirm'),
    path('recovery/done/', views.PasswordResetCompleteView.as_view(), name='password_recovery_complete'),
]