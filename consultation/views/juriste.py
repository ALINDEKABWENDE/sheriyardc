from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.models import JuristeProfile
from consultation.models import RendezVous, Question, AppelVideo


@login_required
def dashboard_juriste(request):
    juriste = request.user.juriste_profile
    rdvs = juriste.rdvs.all()
    appels = juriste.appels_video.all()
    questions = Question.objects.filter(statut='ouverte')

    return render(request, 'accounts/dashboard.html', {
        'rdvs': rdvs,
        'appels': appels,
        'questions': questions,
    })
