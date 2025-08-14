from django.urls import path
from consultation.views import citoyen

app_name = 'citoyen'  # ← important pour le namespace

urlpatterns = [
    path('dashboard/', citoyen.dashboard, name='dashboard'),
    path('mes-demandes/', citoyen.mes_demandes, name='mes_demandes'),
    path('prendre-rdv/', citoyen.prendre_rdv, name='prendre_rdv'),
    path('poser-question/', citoyen.poser_question, name='poser_question'),
]
