from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.contrib import messages
from .models import JuristeProfile, UserProfile
from .forms import CitoyenSignupForm
from chat.models import Conversation
from documents.models import Document
from django.contrib.auth import login
from django.contrib import messages
from .forms import CitoyenSignupForm

def signup_citoyen(request):
    form = CitoyenSignupForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()  # crée le User et le UserProfile
            login(request, user)  # connecte automatiquement
            messages.success(request, "✅ Bienvenue ! Votre compte citoyen a été créé avec succès.")
            return redirect('accounts:voir_profil_citoyen')
        else:
            messages.error(request, "❌ Veuillez corriger les erreurs du formulaire.")

    return render(request, 'accounts/signup_citoyen.html', {
        'form': form
    })


# =============================
#        AUTHENTIFICATION
# =============================

@require_http_methods(["GET", "POST"])
def login_citoyen_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            try:
                profile = user.profile
                if profile.role == "citoyen":
                    return redirect("cabinet:accueil")
                else:
                    return redirect("accounts:juriste_dashboard")
            except UserProfile.DoesNotExist:
                messages.error(request, "Profil utilisateur introuvable.")
                return redirect("accounts:signup_citoyen")
        else:
            messages.error(request, "Nom ou mot de passe incorrect.")

    return render(request, "accounts/login_citoyen.html")

def login_juriste(request):
    return redirect('accounts:login')

def login_citoyen(request):
    return redirect('accounts:signup_citoyen')

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("cabinet:accueil")
        else:
            return render(request, "accounts/login.html", {
                "error": "Nom ou mot de passe incorrect."
            })

    return render(request, "accounts/login.html")

@require_http_methods(["GET", "POST"])
def logout_view(request):
    auth_logout(request)
    return redirect("cabinet:accueil")

# =============================
#        INSCRIPTION
# =============================

def signup_choice(request):
    return render(request, 'accounts/signup_choice.html')



def signup_juriste(request):
    professions = ["Avocat", "Magistrat", "Notaire", "Huissier"]
    return render(request, 'accounts/register.html', {
        "professions": professions
    })

def register_juriste(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        profession = request.POST.get("profession", "").strip()
        speciality = request.POST.get("speciality", "").strip()
        city = request.POST.get("city", "").strip()
        institution = request.POST.get("institution", "").strip()
        bio = request.POST.get("bio", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        photo = request.FILES.get("photo")
        sexe = request.POST.get("sexe")
        date_naissance = request.POST.get("date_naissance")

        if not full_name or not password:
            return render(request, "accounts/register.html", {
                "error": "Nom complet et mot de passe sont requis.",
                "professions": ["Avocat", "Magistrat", "Notaire", "Huissier"]
            })

        if User.objects.filter(username=full_name).exists():
            return render(request, "accounts/register.html", {
                "error": "Ce nom est déjà utilisé.",
                "professions": ["Avocat", "Magistrat", "Notaire", "Huissier"]
            })

        user = User.objects.create_user(
            username=full_name,
            email=email,
            password=password
        )

        JuristeProfile.objects.create(
            user=user,
            profession=profession,
            specialite=speciality,
            ville=city,
            institution=institution,
            bio=bio,
            photo=photo if photo else None,
            sexe=sexe,
            date_naissance=date_naissance or None
        )

        login(request, user)
        return redirect("accounts:juriste_dashboard")

    return redirect("accounts:signup_juriste")

# =============================
#        PROFIL JURISTE
# =============================

@login_required(login_url='/login/')
def modifier_profil(request):
    user = request.user
    juriste = getattr(user, 'juriste_profile', None)

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        profession = request.POST.get('profession', '').strip()
        specialite = request.POST.get('specialite', '').strip()
        ville = request.POST.get('ville', '').strip()
        institution = request.POST.get('institution', '').strip()
        bio = request.POST.get('bio', '').strip()
        photo = request.FILES.get('photo')
        sexe = request.POST.get('sexe')
        date_naissance = request.POST.get('date_naissance') or None

        user.username = full_name
        user.email = email
        user.save()

        if juriste:
            juriste.profession = profession
            juriste.specialite = specialite
            juriste.ville = ville
            juriste.institution = institution
            juriste.bio = bio
            juriste.sexe = sexe
            juriste.date_naissance = date_naissance
            if photo:
                juriste.photo = photo
            juriste.save()
        else:
            JuristeProfile.objects.create(
                user=user,
                profession=profession,
                specialite=specialite,
                ville=ville,
                institution=institution,
                bio=bio,
                photo=photo if photo else None,
                sexe=sexe,
                date_naissance=date_naissance
            )

        messages.success(request, "Profil mis à jour avec succès.")
        return redirect('accounts:voir_profil')

    return render(request, 'accounts/modifier_profil.html', {
        'user': user,
        'juriste': juriste,
        'titre_page': 'Modifier mon profil professionnel',
    })

@login_required(login_url='/login/')
def voir_profil(request):
    juriste = getattr(request.user, 'juriste_profile', None)
    return render(request, "accounts/profil.html", {
        "juriste": juriste,
        "user": request.user
    })

# =============================
#        PROFIL CITOYEN
# =============================

@login_required(login_url='/login/')
def voir_profil_citoyen(request):
    citoyen = getattr(request.user, 'profile', None)
    return render(request, "accounts/profil_citoyen.html", {
        "citoyen": citoyen,
        "user": request.user
    })

@login_required(login_url='/login/')
def modifier_profil_citoyen(request):
    user = request.user
    citoyen = getattr(user, 'profile', None)

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        sexe = request.POST.get('sexe')
        date_naissance = request.POST.get('date_naissance') or None
        ville = request.POST.get('ville', '').strip()
        profession = request.POST.get('profession', '').strip()
        telephone = request.POST.get('telephone', '').strip()
        bio = request.POST.get('bio', '').strip()
        photo = request.FILES.get('photo')

        parts = full_name.split()
        user.first_name = parts[0]
        user.last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
        user.email = email
        user.save()

        citoyen.sexe = sexe
        citoyen.date_naissance = date_naissance
        citoyen.ville = ville
        citoyen.profession = profession
        citoyen.telephone = telephone
        citoyen.bio = bio
        if photo:
            citoyen.photo = photo
        citoyen.save()

        messages.success(request, "Profil citoyen mis à jour avec succès.")
        return redirect('accounts:voir_profil_citoyen')

    return render(request, 'accounts/modifier_profil_citoyen.html', {
        'user': user,
        'citoyen': citoyen,
        'titre_page': 'Modifier mon profil citoyen',
    })

# =============================
#        DASHBOARD JURISTE
# =============================

@login_required(login_url='/login/')
def juriste_dashboard(request):
    user = request.user
    juriste = getattr(user, 'juriste_profile', None)

    stats = [
        {"label": "Documents récents", "value": Document.objects.filter(auteur=user).count(), "color": "primary"},
        {"label": "Utilisateurs enregistrés", "value": User.objects.count(), "color": "success"},
        {"label": "Profil complet", "value": "Oui" if juriste else "Non", "color": "warning"},
        {"label": "Dernière connexion", "value": timezone.now().strftime("%d/%m/%Y %H:%M"), "color": "info"},
    ]

    documents = Document.objects.filter(auteur=user).order_by("-date_creation")[:5]

    return render(request, "accounts/dashboard.html", {
        "user": user,
        "juriste": juriste,
        "stats": stats,
        "documents": documents,
    })

# =============================
#        PAGE D'ACCUEIL
# =============================

def accueil(request):
    juristes = JuristeProfile.objects.select_related('user').order_by('-created_at')[:6]
    return render(request, "accueil.html", {
        "juristes": juristes
    })

# =============================
#        DÉTAILS JURISTE
# =============================

def juriste_detail(request, id):
    juriste = get_object_or_404(JuristeProfile, pk=id)
    return render(request, "accounts/detail.html", {
        "juriste": juriste
    })

