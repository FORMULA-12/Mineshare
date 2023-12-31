from django.contrib.auth import views
from django.urls import path, reverse_lazy
from .views import *


app_name = 'home'

urlpatterns = [
    path('', home, name='home'),
    path('terms/', terms, name='terms'),
    path('privacy/', privacy, name='privacy'),
    path('about/', about, name='about'),
    path('partners/', partners, name='partners'),
]