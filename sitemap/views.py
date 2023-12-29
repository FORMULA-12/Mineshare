from django.http import HttpResponse
from django.shortcuts import render


def sitemap(request):
    return render(request, 'sitemap.xml', content_type='text/xml')


def robots(request):
    return render(request, 'robots.txt', content_type='text/plain')
