from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from consultation.models import RendezVous, Question, AppelVideo
from consultation.forms import RendezVousForm, QuestionForm

@login_required
def prendre_rdv(request):
    if request.method == 'POST':
        form = RendezVousForm(request.POST)
        if form.is_valid():
            rdv = form.save(commit=False)
            rdv.utilisateur = request.user
            rdv.save()
            return redirect('citoyen:dashboard')  # ← corrigé
    else:
        form = RendezVousForm()

    return render(request, 'consultation/prendre_rdv.html', {'form': form})

@login_required
def poser_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.utilisateur = request.user
            question.save()
            return redirect('citoyen:dashboard')  # ← corrigé
    else:
        form = QuestionForm()

    return render(request, 'consultation/poser_question.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    rdvs = RendezVous.objects.filter(utilisateur=user)
    questions = Question.objects.filter(utilisateur=user)
    appels = AppelVideo.objects.filter(utilisateur=user)

    return render(request, 'consultation/dashboard_citoyen.html', {
        'rdvs': rdvs,
        'questions': questions,
        'appels': appels,
    })

@login_required
def mes_demandes(request):
    return render(request, 'citoyen/mes_demandes.html')
