import os

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import FileResponse
from django.urls import reverse
from django.template import loader
from django.conf import settings


def home(request):
    print(settings.BASE_DIR)
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def terms(request):
    return FileResponse(open(os.path.join(settings.BASE_DIR, 'templates/terms.pdf'), 'rb'), content_type='application/pdf')


def privacy(request):
    return FileResponse(open(os.path.join(settings.BASE_DIR, 'templates/privacy.pdf'), 'rb'), content_type='application/pdf')


def partners(request):
    return render(request, 'partners.html')


def error404(request, exception):
    return render(request, 'error404.html', status=404)


def error500(request, *args, **argv):
    return render(request, 'error404.html', status=500)
