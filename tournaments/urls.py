from django.contrib.auth import views
from django.urls import path, reverse_lazy
from .views import *
from . import views

app_name = 'tournaments'

urlpatterns = [
    path('bedwars/', bedwars, name='bedwars'),
]
