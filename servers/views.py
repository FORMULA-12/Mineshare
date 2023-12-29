from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from .models import *
from django.db.models import Q
from profile.forms import Register
from profile.models import ServersBuffer


def servers(request):
    form_reg = Register
    template = loader.get_template('servers.html')
    model = Servers.objects.filter(block=False).order_by('-rate')

    for _x in range(len(model)):

        if len(model[_x].description) >= 600:
            if not model[_x].description_rate_add:
                model[_x].rate += 5
                model[_x].description_rate_add = True
                model[_x].save()
        elif len(model[_x].description) < 600:
            if model[_x].description_rate_add:
                model[_x].rate -= 5
                model[_x].description_rate_add = False
                model[_x].save()

        if model[_x].icon.image == 'posters/127db10f-4eab-41f7-83e5-781b00a5a42f.gif':
            if model[_x].banner_rate_add:
                model[_x].rate -= 5
                model[_x].banner_rate_add = False
                model[_x].save()
        else:
            if not model[_x].banner_rate_add:
                model[_x].rate += 5
                model[_x].banner_rate_add = True
                model[_x].save()

        if model[_x].illustrations.count() <= 0:
            if model[_x].illustrations_rate_add:
                model[_x].rate -= 5
                model[_x].illustrations_rate_add = False
                model[_x].save()
        else:
            if not model[_x].illustrations_rate_add:
                model[_x].rate += 5
                model[_x].illustrations_rate_add = True
                model[_x].save()

        if model[_x].premium_status:
            if not model[_x].premium_rate_add:
                model[_x].rate += 10
                model[_x].premium_rate_add = True
                model[_x].save()
        elif not model[_x].premium_status:
            if model[_x].premium_rate_add:
                model[_x].rate -= 10
                model[_x].premium_rate_add = False
                model[_x].save()

        if model[_x].boost_status:
            if not model[_x].boost_rate_add:
                model[_x].rate += 50
                model[_x].boost_rate_add = True
                model[_x].save()
        elif not model[_x].boost_status:
            if model[_x].boost_rate_add:
                model[_x].rate -= 50
                model[_x].boost_rate_add = False
                model[_x].save()

        if model[_x].online_status:
            if not model[_x].online_rate_add:
                model[_x].rate += 10
                model[_x].online_rate_add = True
                model[_x].save()
        elif not model[_x].online_status:
            if model[_x].online_rate_add:
                model[_x].rate -= 10
                model[_x].online_rate_add = False
                model[_x].save()

        if model[_x].current_players >= 5:
            if not model[_x].activity_rate_add:
                model[_x].rate += 10
                model[_x].activity_rate_add = True
                model[_x].save()
        elif model[_x].current_players < 5:
            if model[_x].activity_rate_add:
                model[_x].rate -= 10
                model[_x].activity_rate_add = False
                model[_x].save()

        if model[_x].current_players >= 50:
            if not model[_x].popularity_rate_add:
                model[_x].rate += 10
                model[_x].popularity_rate_add = True
                model[_x].save()
        elif model[_x].current_players < 50:
            if model[_x].popularity_rate_add:
                model[_x].rate -= 10
                model[_x].popularity_rate_add = False
                model[_x].save()

        if model[_x].current_players >= 500:
            if not model[_x].superiority_rate_add:
                model[_x].rate += 10
                model[_x].superiority_rate_add = True
                model[_x].save()
        elif model[_x].current_players < 500:
            if model[_x].superiority_rate_add:
                model[_x].rate -= 10
                model[_x].superiority_rate_add = False
                model[_x].save()

        if model[_x].verification:
            if not model[_x].verification_rate_add:
                model[_x].rate += 10
                model[_x].verification_rate_add = True
                model[_x].save()
        elif not model[_x].verification:
            if model[_x].verification_rate_add:
                model[_x].rate -= 10
                model[_x].verification_rate_add = False
                model[_x].save()

    context = {
        'servers': model[:30],
        'register_form': form_reg,
    }

    if request.GET.get('page'):
        page = int((request.GET.get('page')))
        object_list = Servers.objects.filter(block=False).order_by('-rate')[(page * 30 - 30):(page * 30)]
        context = {
            'servers': object_list,
            'register_form': form_reg,
        }

    elif request.GET.get('search'):
        query = (request.GET.get('search')).lower()
        object_list = Servers.objects.filter(block=False).filter(
            Q(name__contains=query) | Q(description__contains=query) | Q(ip__contains=query)
        ).order_by('-rate')
        context = {
            'servers': object_list,
            'register_form': form_reg,
        }

    elif request.GET.get('version'):
        query = request.GET.get('version')
        object_list = Servers.objects.filter(block=False).filter(
            Q(version__contains=query)
        ).order_by('-rate')
        context = {
            'servers': object_list,
            'register_form': form_reg,
        }
        return HttpResponse(template.render(context, request))

    elif request.GET.get('mode'):
        query = request.GET.get('mode')
        print(query)
        object_list = Servers.objects.filter(block=False).filter(
            Q(mode__contains=query)
        ).order_by('-rate')
        context = {
            'servers': object_list,
            'register_form': form_reg,
        }
        return HttpResponse(template.render(context, request))

    elif request.GET.get('attribute'):
        query = request.GET.get('attribute')
        print(query)
        object_list = Servers.objects.filter(block=False).filter(
            Q(attributes__title__contains=query)
        ).order_by('-rate')
        context = {
            'servers': object_list,
            'register_form': form_reg,
        }
        return HttpResponse(template.render(context, request))

    elif request.GET.get('online'):
        query = request.GET.get('online')
        print(query)

        if query == 'Больше':
            object_list = Servers.objects.all().order_by('-current_players')
        elif query == 'Меньше':
            object_list = Servers.objects.all().order_by('current_players')
        else:
            object_list = Servers.objects.all().order_by('-current_players')

        context = {
            'servers': object_list,
            'register_form': form_reg,
        }
        return HttpResponse(template.render(context, request))

    elif request.GET.get('rate'):
        query = request.GET.get('rate')
        print(query)

        if query == 'Больше':
            object_list = Servers.objects.all().order_by('-rate')
        elif query == 'Меньше':
            object_list = Servers.objects.all().order_by('rate')
        else:
            object_list = Servers.objects.all().order_by('-rate')

        context = {
            'servers': object_list,
            'register_form': form_reg,
        }
        return HttpResponse(template.render(context, request))

    elif request.GET.get('date'):
        query = request.GET.get('date')
        print(query)

        if query == 'Новые':
            object_list = Servers.objects.all().order_by('-date')
        elif query == 'Старые':
            object_list = Servers.objects.all().order_by('date')
        else:
            object_list = Servers.objects.all().order_by('-date')

        context = {
            'servers': object_list,
            'register_form': form_reg,
        }
        return HttpResponse(template.render(context, request))

    return HttpResponse(template.render(context, request))


def create_server(request):
    template = loader.get_template('create.html')
    data_from_check = ServersBuffer.objects.filter(Q(creator=request.user.id)).order_by('-date').first()

    for_create = Servers()

    tags_all = Tags.objects.all()
    context = {
        'name': data_from_check,
        'tags_all': tags_all,
    }

    if request.method == "POST":
        tag_list = []

        for_create.owner_id = request.user.id
        for_create.description = request.POST.get('desc')

        blacklist = ['пидарас', 'пидарасы', 'пидор', 'пидоры', 'педик', 'пидр', 'гомик', 'faggot', 'хохол', 'nigger',
                     'nigga',
                     'naga', 'ниггер', 'нига', 'нигер', 'нигга', 'нага', 'даун', 'аутист', 'шлюха', 'хуй', 'хуйло',
                     'пидар',
                     'лох', 'долбоеб', 'долбаеб', 'пизда', 'пиздец']

        if any(bad_word in request.POST.get('desc') for bad_word in blacklist):
            for_create.block = True

        for_create.ip = data_from_check.server_ip
        for_create.port = data_from_check.server_port

        if request.POST.get('name'):
            for_create.name = request.POST.get('name')
        else:
            for_create.name = data_from_check.name

        if request.POST.get('get_type') == "Анархия":
            for_create.mode = "ANARCHY"
        elif request.POST.get('get_type') == "MMO-RPG":
            for_create.mode = "MMORPG"
        elif request.POST.get('get_type') == "Мини-игры":
            for_create.mode = "MINIGAMES"
        elif request.POST.get('get_type') == "Приключение":
            for_create.mode = "ADVENTURE"
        elif request.POST.get('get_type') == "Строительство":
            for_create.mode = "CONSTRUCTION"
        else:
            for_create.mode = "VANILLA"

        if request.POST.get('get_version') == "1.8.X":
            for_create.version = "1.8"
        elif request.POST.get('get_version') == "1.9.X":
            for_create.version = "1.9"
        elif request.POST.get('get_version') == "1.10.X":
            for_create.version = "1.10"
        elif request.POST.get('get_version') == "1.11.X":
            for_create.version = "1.11"
        elif request.POST.get('get_version') == "1.12.X":
            for_create.version = "1.12"
        elif request.POST.get('get_version') == "1.13.X":
            for_create.version = "1.13"
        elif request.POST.get('get_version') == "1.14.X":
            for_create.version = "1.14"
        elif request.POST.get('get_version') == "1.15.X":
            for_create.version = "1.15"
        elif request.POST.get('get_version') == "1.16.X":
            for_create.version = "1.16"
        elif request.POST.get('get_version') == "1.17.X":
            for_create.version = "1.17"
        elif request.POST.get('get_version') == "1.18.X":
            for_create.version = "1.18"
        elif request.POST.get('get_version') == "1.19.X":
            for_create.version = "1.19"
        else:
            for_create.version = "1.7"

        print(request.POST.get('get_version'))

        if request.POST.get('get_license') == "Лицензия":
            for_create.license = True
        else:
            for_create.license = False

        for tag in tags_all:
            try:
                tag_state = request.POST.get(f'tag_{tag.id}')

                if tag_state == 'on':
                    tag_list.append(tag.id)

            except Exception as e:
                pass

        for_create.save()
        for tag_id in tag_list:
            for_create.attributes.add(tag_id)

        for_create.save()
        trash = ServersBuffer.objects.filter(creator_id=request.user.id)
        for record in trash:
            record.delete()
        return redirect('account:main')

    return HttpResponse(template.render(context, request))


def about(request, pk):
    server = Servers.objects.filter(pk=pk)
    template = loader.get_template('server.html')
    form_reg = Register
    tags = server[0].attributes.all()
    illustrations = server[0].illustrations.all()
    context = {
        'server': server,
        'tags': tags,
        'register_form': form_reg,
        'illustrations': illustrations
    }
    return HttpResponse(template.render(context, request))


def signup_redirect(request):
    return redirect('account:main')
