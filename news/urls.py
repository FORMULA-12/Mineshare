from django.contrib.auth import views
from django.urls import path, reverse_lazy
from .views import *

app_name = 'news'

urlpatterns = [
    path('', news, name='news'),
]
