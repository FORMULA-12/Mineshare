from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordResetView
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth import login as auth_login
from mcstatus import JavaServer
from servers.models import *
from profile.forms import Register, PassEmailForm, PictureForm
from django.db.models import Q
from .models import ServersBuffer
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


def register(request):
    if request.method == 'POST':

        user_form = Register(request.POST)

        username = user_form.data.get('username')
        try:
            user = User.objects.get(username=username)

            response = JsonResponse({"error": "user exists"})
            response.status_code = 403
            return response
        except:
            pass

        if user_form.is_valid():
            new_user = user_form.save(commit=False)

            new_user.set_password(user_form.cleaned_data['password'])

            new_user.save()
            response = JsonResponse({"success": 'Okay'})
            response.status_code = 200
            return response
    else:
        user_form = Register
        response = JsonResponse({"error": "unknown"})
        response.status_code = 403
        return response


def status_server(request):
    if request.method == "POST":
        try:
            if request.POST.get('srv_ip') and request.POST.get('srv_name'):

                ip_check = Servers.objects.filter(Q(ip=request.POST.get('srv_ip')))

                if len(ip_check) > 0:
                    context = None
                    template = loader.get_template('error404.html')
                    return HttpResponse(template.render(context, request))

                if request.POST.get('srv_port').strip() == "25565":
                    server = JavaServer.lookup(request.POST.get('srv_ip').strip())
                    ServersBuffer.objects.create(creator_id=request.user.id,
                                                 name=request.POST.get('srv_name').strip(),
                                                 server_ip=request.POST.get('srv_ip').strip())
                elif not request.POST.get('srv_port'):
                    server = JavaServer.lookup(request.POST.get('srv_ip').strip())
                    ServersBuffer.objects.create(creator_id=request.user.id,
                                                 name=request.POST.get('srv_name').strip(),
                                                 server_ip=request.POST.get('srv_ip').strip())
                else:
                    server = JavaServer.lookup(
                        request.POST.get('srv_ip').strip() + ":" + request.POST.get('srv_port').strip())
                    ServersBuffer.objects.create(creator_id=request.user.id,
                                                 name=request.POST.get('srv_name').strip(),
                                                 server_ip=request.POST.get('srv_ip').strip(),
                                                 server_port=request.POST.get('srv_port').strip())

                status = server.status()

                if status:
                    response = JsonResponse({"success": 'Okay'})
                    response.status_code = 200
                    return response

        except Exception as e:
            print(e)

    response = JsonResponse({"error": "Server is not response"})
    response.status_code = 403
    return response


@login_required()
def account(request):
    template = loader.get_template('account.html')
    model = Servers.objects.filter(owner=request.user.id).order_by('id')
    context = {
        'servers': model,
    }
    return HttpResponse(template.render(context, request))


def login(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            response = JsonResponse({"error": "user does not exist"})
            response.status_code = 403
            return response

        account = authenticate(username=username, password=password)
        if account:
            auth_login(request, account)
            response = JsonResponse({"success": "ok"})
            response.status_code = 200
            return response

    response = JsonResponse({"error": "unknown"})
    response.status_code = 403
    return response


def main_page(request):
    template = loader.get_template('main.html')
    form_reg = Register
    context = {
        'servers': 'pass',
        'register_form': form_reg,
    }

    return HttpResponse(template.render(context, request))


def edit_server(request, pk):
    for_redact = Servers.objects.get(pk=pk)
    template = loader.get_template('edit.html')
    tags = for_redact.attributes.all()
    tags_all = Tags.objects.all()

    form_picture = PictureForm(initial={'title': for_redact.icon, 'image': for_redact.icon.image})

    context = {
        'server': for_redact,
        'tags_server': tags,
        'tags_all': tags_all,
        'form_picture': form_picture
    }

    if request.method == "POST":
        form_picture = PictureForm(request.POST, request.FILES)
        if form_picture.is_valid():
            picture = form_picture.save()
            for_redact.icon = picture

        if request.FILES.get('illustrations'):
            if Servers.objects.get(pk=pk).illustrations.count() < 6:
                for illustration in request.FILES.getlist('illustrations'):
                    title = Servers.objects.get(pk=pk).ip
                    image = illustration
                    record = Illustrations(title=title, image=image)
                    record.save()
                    Servers.objects.get(pk=pk).illustrations.add(record)

        for_redact.description = request.POST.get('desc')

        blacklist = ['пидарас', 'пидарасы', 'пидор', 'пидоры', 'педик', 'пидр', 'гомик', 'faggot', 'хохол', 'nigger',
                     'nigga', 'naga', 'ниггер', 'нига', 'нигер', 'нигга', 'нага', 'даун', 'аутист', 'шлюха', 'хуй',
                     'хуйло', 'пидар', 'лох', 'долбоеб', 'долбаеб', 'пизда', 'пиздец']

        if any(bad_word in request.POST.get('desc') for bad_word in blacklist):
            for_redact.block = True

        if request.POST.get('get_type') == "Анархия":
            for_redact.mode = "ANARCHY"
        elif request.POST.get('get_type') == "MMO-RPG":
            for_redact.mode = "MMORPG"
        elif request.POST.get('get_type') == "Мини-игры":
            for_redact.mode = "MINIGAMES"
        elif request.POST.get('get_type') == "Приключение":
            for_redact.mode = "ADVENTURE"
        elif request.POST.get('get_type') == "Строительство":
            for_redact.mode = "CONSTRUCTION"
        else:
            for_redact.mode = "VANILLA"

        if request.POST.get('get_version') == "1.8.X":
            for_redact.version = "1.8"
        elif request.POST.get('get_version') == "1.9.X":
            for_redact.version = "1.9"
        elif request.POST.get('get_version') == "1.10.X":
            for_redact.version = "1.10"
        elif request.POST.get('get_version') == "1.11.X":
            for_redact.version = "1.11"
        elif request.POST.get('get_version') == "1.12.X":
            for_redact.version = "1.12"
        elif request.POST.get('get_version') == "1.13.X":
            for_redact.version = "1.13"
        elif request.POST.get('get_version') == "1.14.X":
            for_redact.version = "1.14"
        elif request.POST.get('get_version') == "1.15.X":
            for_redact.version = "1.15"
        elif request.POST.get('get_version') == "1.16.X":
            for_redact.version = "1.16"
        elif request.POST.get('get_version') == "1.17.X":
            for_redact.version = "1.17"
        elif request.POST.get('get_version') == "1.18.X":
            for_redact.version = "1.18"
        elif request.POST.get('get_version') == "1.19.X":
            for_redact.version = "1.19"
        else:
            for_redact.version = "1.7"

        if request.POST.get("website"):
            if "http" in request.POST.get("website") or "https" in request.POST.get("website"):
                for_redact.website = request.POST.get("website").strip()
                for_redact.launcher = True
        else:
            for_redact.website = ""
            for_redact.launcher = False

        if request.POST.get("gradient_color"):
            for_redact.premium_color = Colors.objects.filter(title__contains=request.POST.get('gradient_color'))[0]

        if request.POST.get('get_license') == "Лицензия":
            for_redact.license = True
        else:
            for_redact.license = False

        if request.POST.get('name'):
            for_redact.name = request.POST.get('name')
        else:
            for_redact.name = "Без названия"

        for_redact.save()
        for tag in tags_all:

            try:
                tag_state = request.POST.get(f'tag_{tag.id}')

                if tag_state == 'on':
                    for_redact.attributes.add(Tags.objects.get(pk=tag.id))
                    for_redact.save()
                else:
                    for_redact.attributes.remove(Tags.objects.get(pk=tag.id))
                    for_redact.save()

            except Exception as e:
                pass

        return redirect('account:main')

    return HttpResponse(template.render(context, request))


class PasswordResetCustom(PasswordResetView):
    form_class = PassEmailForm


def delete_server(request, pk):
    del_serv = Servers.objects.get(pk=pk)
    del_serv.delete()
    return redirect('account:main')


def change_username(request):
    if request.method == 'POST':
        old_username = request.POST.get('old_username')
        new_username = request.POST.get('new_username')

        if new_username == '':
            return redirect('account:main')
        else:
            if User.objects.filter(username=new_username).exists():
                response = JsonResponse({"error": "user exists"})
                response.status_code = 403
                return response
            else:
                user = User.objects.get(username=old_username)
                user.username = new_username
                user.save()

                ip = request.META.get('REMOTE_ADDR')
                html = f'''
                <style>@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@500&display=swap');</style>
                <div style="width:60%;background:#F3F7FC;padding-top:5%;padding-left:6%;padding-right:8%;padding-bottom:6%;">
                <img style="width:15%;" src="https://mineshare.top/static/ASSETS/favicon.png">
                <p style="color:#3A4E57;font-size:280%;font-weight:600;margin-top:5%;margin-bottom:0;">Здравствуйте, {old_username}</p>
                <p style="color:#3A4E57;font-size:150%;font-weight:500;margin-top:2.5%;">Ваш новый логин, необходимый для входа в аккаунт:</p>
                <h1 style="background:#fff;color:#11B2FF;font-family:'Roboto',sans-serif;font-size:420%;text-align:center;padding-top:18px;padding-bottom:20px;margin-top:2%;">{new_username}</h1>
                <p style="color:#3A4E57;font-size:150%;font-weight:500;margin-top:10%;">Вы получили это письмо из-за успешной попытки изменения логина вашего аккаунта из браузера по адресу {ip}</p>
                <p style="color:#3A4E57;font-size:150%;font-weight:500;margin-top:2.5%;">Если вы не пытались изменить никнейм своего аккаунта - немедленно обратитесь к администрации мониторинга и сообщите об этом.</p>
                </div>
                '''

                send_mail('Вы успешно изменили никнейм 👌', '', settings.EMAIL_HOST_USER, [f'{request.user.email}'], html_message=html)

                return redirect('account:logout')

    return redirect('account:main')