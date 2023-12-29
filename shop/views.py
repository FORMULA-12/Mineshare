from django.http import HttpResponse
from django.template import loader
from profile.forms import Register


def shop(request):
    form_reg = Register
    template = loader.get_template('shop.html')
    context = {
        'server': 'shop',
        'register_form': form_reg,
    }
    return HttpResponse(template.render(context, request))
