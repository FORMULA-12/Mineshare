from django.http import HttpResponse
from django.shortcuts import redirect
from tournaments.models import Bedwars
from profile.forms import Register
from django.template import loader


def bedwars(request):
    if request.method == 'POST':
        team = request.POST.get('team-name')
        contact = request.POST.get('contact')
        player1 = request.POST.get('player1')
        player2 = request.POST.get('player2')
        player3 = request.POST.get('player3')
        player4 = request.POST.get('player4')

        if request.POST.get('description'):
            description = request.POST.get('description')
        else:
            description = "Описание отсутствует"

        if Bedwars.objects.filter(owner=request.user).exists():
            return redirect('tournaments:bedwars')
        else:
            record = Bedwars.objects.create(owner=request.user, team=team, contact=contact, description=description,
                                            player1=player1, player2=player2, player3=player3, player4=player4)
            record.save()
            return redirect('tournaments:bedwars')

    form_reg = Register
    tournament_counter = Bedwars.objects.count()
    if request.user.is_authenticated:
        tournament_request_send = Bedwars.objects.filter(owner=request.user).exists()
    else:
        tournament_request_send = False
    template = loader.get_template('bedwars.html')
    context = {
        'register_form': form_reg,
        'tournament_counter': tournament_counter,
        'tournament_request_send': tournament_request_send
    }

    return HttpResponse(template.render(context, request))
