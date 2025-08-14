from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import DocumentGenere

@login_required
def documents_liste(request):
    """
    Vue listant les documents générés par l'utilisateur connecté.
    Trié par date décroissante pour une UX optimale.
    Accessible uniquement aux utilisateurs authentifiés.
    """
    documents = DocumentGenere.objects.filter(utilisateur=request.user).order_by('-date_creation')

    context = {
        'documents': documents,
        'titre_page': "Mes documents générés",
    }
    return render(request, 'documents/documents_liste.html', context)


@login_required
def upload_document(request):
    """
    Vue d'affichage du formulaire de téléversement de document.
    Accessible uniquement aux utilisateurs authentifiés.
    Préparée pour être connectée à un Form ou widget.
    """
    return render(request, 'documents/upload_document.html', {'titre_page': "Ajouter un document"})
