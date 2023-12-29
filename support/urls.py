from django.urls import path, reverse_lazy
from .views import *


app_name = 'support'

urlpatterns = [
    path('', support, name='support'),
]