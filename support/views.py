from django.http import HttpResponse
from django.shortcuts import render
from.models import Support
from django.template import loader
from profile.forms import Register


def support(request):
    template = loader.get_template('support.html')
    form_reg = Register
    context = {
        'pass': 'pass',
        'register_form': form_reg,
    }
    if request.method == "POST":

        user_id = request.user
        name_from_user = request.POST.get('name')
        email = request.POST.get('email')
        text = request.POST.get('text')
        if user_id and email and text:
            model = Support(name_user=user_id, name_from_user=name_from_user, email=email, text=text)
            model.save()
            template = loader.get_template('answer.html')
            context = {
                'context': 'Ваш запрос успешно отправлен'
            }
            return HttpResponse(template.render(context, request))
    return HttpResponse(template.render(context, request))
