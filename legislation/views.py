from django.db.models import Q
from django.shortcuts import render
from .models import TexteLegal
from django.http import HttpResponse

def simple_view(request):
    return HttpResponse("OK")

def recherche_lois(request):
    query = request.GET.get("q", "").strip()
    resultats = []

    if query:
        resultats = TexteLegal.objects.filter(
            Q(titre__icontains=query) |
            Q(contenu__icontains=query)
        )
    
    return render(request, "legislation/recherche.html", {
        "query": query,
        "resultats": resultats
    })



# Create your views here.
