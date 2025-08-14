from django.shortcuts import render
from dossiers.models import Dossier 
from legislation.models import TexteLegal
from accounts.models import JuristeProfile
from actualites.models import ArticleActualite

def accueil(request):
    """
    Vue pour la page d'accueil.
    Affiche la version adaptée selon que l'utilisateur est connecté ou non.
    """
    context = {
        'lois_count': TexteLegal.objects.count(),
        'juristes_count': JuristeProfile.objects.count(),
        'actualites': ArticleActualite.objects.all().order_by('-date_publication')[:6],
    }

    # Pour les utilisateurs connectés, tu peux aussi passer des dossiers, etc.
    if request.user.is_authenticated:
        context['dossiers_utilisateur'] = Dossier.objects.filter(utilisateur=request.user)

    return render(request, 'cabinet/accueil.html', context)
