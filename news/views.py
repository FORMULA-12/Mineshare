from django.http import HttpResponse
from django.shortcuts import render
from profile.forms import Register
# Create your views here.
from django.template import loader
from .models import News


def news(request):
    form_reg = Register
    template = loader.get_template('news.html')
    model = News.objects.order_by('-date')
    context = {
        'news': model,
        'register_form': form_reg,
    }

    return HttpResponse(template.render(context, request))
