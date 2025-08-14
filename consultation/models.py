from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from accounts.models import JuristeProfile

# 📅 Rendez-vous entre citoyen et juriste
class RendezVous(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rdvs')
    juriste = models.ForeignKey(JuristeProfile, on_delete=models.CASCADE, related_name='rdvs')
    date = models.DateTimeField()
    motif = models.TextField()
    statut = models.CharField(
        max_length=20,
        choices=[
            ('en_attente', _('En attente')),
            ('confirmé', _('Confirmé')),
            ('annulé', _('Annulé')),
            ('terminé', _('Terminé')),
        ],
        default='en_attente'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def est_futur(self):
        return self.date > timezone.now()

    def __str__(self):
        return f"RDV {self.utilisateur.username} avec {self.juriste.user.username} le {self.date.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        ordering = ['-date']


# ❓ Question posée par un citoyen
class Question(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    objet = models.CharField(max_length=255, default="Sans objet")
    contenu = models.TextField()
    categorie = models.CharField(
        max_length=100,
        choices=[
            ('droit_civil', _('Droit civil')),
            ('droit_penal', _('Droit pénal')),
            ('droit_travail', _('Droit du travail')),
            ('autre', _('Autre')),
        ],
        default='autre'
    )
    est_payante = models.BooleanField(default=False)
    statut = models.CharField(
        max_length=20,
        choices=[
            ('ouverte', _('Ouverte')),
            ('répondue', _('Répondue')),
            ('fermée', _('Fermée')),
        ],
        default='ouverte'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def est_active(self):
        return self.statut == 'ouverte'

    def __str__(self):
        return f"{self.objet} - {self.statut}"

    class Meta:
        ordering = ['-created_at']


# ✅ Réponse d’un juriste à une question
class Réponse(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='réponse')
    juriste = models.ForeignKey(JuristeProfile, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_reponse = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Réponse à Q{self.question.id} par {self.juriste.user.username}"


# 🎥 Appel vidéo programmé entre citoyen et juriste
class AppelVideo(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appels_video')
    juriste = models.ForeignKey(JuristeProfile, on_delete=models.CASCADE, related_name='appels_video')
    lien = models.URLField()
    date = models.DateTimeField()
    statut = models.CharField(
        max_length=20,
        choices=[
            ('prévu', _('Prévu')),
            ('en_cours', _('En cours')),
            ('terminé', _('Terminé')),
            ('annulé', _('Annulé')),
        ],
        default='prévu'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def est_actif(self):
        return self.statut == 'en_cours' and self.date <= timezone.now()

    def __str__(self):
        return f"Appel {self.utilisateur.username} avec {self.juriste.user.username} - {self.date.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        ordering = ['-date']


# 📨 Conversation pour messages (relation avec consultation.Message si besoin)
class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation entre {', '.join([user.username for user in self.participants.all()])}"

    @property
    def last_message(self):
        return self.messages.order_by('-timestamp').first()


# 📨 Message
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages', default=1)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultation_messages')
    contenu = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message de {self.utilisateur.username} à {self.created_at}"
