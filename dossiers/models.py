
# dossiers/models.py
from django.contrib.auth.models import User
from django.db import models

class Dossier(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    titre = models.CharField(max_length=200)
    description = models.TextField()
    statut = models.CharField(max_length=50, choices=[
        ('En attente', 'En attente'),
        ('Audiencé', 'Audiencé'),
        ('Jugé', 'Jugé'),
        ('Clôturé', 'Clôturé')
    ])
    date_creation = models.DateTimeField(auto_now_add=True)
    date_audience = models.DateField(null=True, blank=True)
    pieces_jointes = models.FileField(upload_to="dossiers/", null=True, blank=True)

# Create your models here.
