from django.shortcuts import render, get_object_or_404, redirect
from .models import Dossier
from .forms import DossierForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def liste_dossiers(request):
    query = request.GET.get("q", "")
    dossiers_list = Dossier.objects.filter(utilisateur=request.user)

    if query:
        dossiers_list = dossiers_list.filter(
            Q(titre__icontains=query) |
            Q(description__icontains=query)
        )

    paginator = Paginator(dossiers_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "dossiers/liste_dossiers.html", {
        "page_obj": page_obj,
        "query": query,
    })

@login_required
def creer_dossier(request):
    if request.method == "POST":
        form = DossierForm(request.POST, request.FILES)
        if form.is_valid():
            dossier = form.save(commit=False)
            dossier.utilisateur = request.user
            dossier.save()
            return redirect("dossiers:liste_dossiers")  # ✅ Correction ici
    else:
        form = DossierForm()
    return render(request, "dossiers/creer.html", {"form": form})
