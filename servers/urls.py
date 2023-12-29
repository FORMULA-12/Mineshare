from django.contrib.auth import views
from django.urls import path, reverse_lazy
from .views import *
from . import views

app_name = 'servers'

urlpatterns = [
    path('', servers, name='servers'),
    path('servers/<pk>/', about, name='about'),
    path('social/signup/', views.signup_redirect, name='signup_redirect'),
]
