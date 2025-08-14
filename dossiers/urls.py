from django.urls import path
from . import views

app_name = 'dossiers'

urlpatterns = [
    path('', views.liste_dossiers, name="liste_dossiers"),
    path('creer/', views.creer_dossier, name='creer_dossier'),
]

