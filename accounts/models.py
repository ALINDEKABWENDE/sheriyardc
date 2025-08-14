from django.db import models
from django.contrib.auth.models import User
from datetime import date

# 🧑‍💼 Profil général lié à chaque utilisateur
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('citoyen', 'Citoyen'),
        ('juriste', 'Juriste'),
    )

    SEXE_CHOICES = (
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('A', 'Autre'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    role = models.CharField("Rôle", max_length=20, choices=ROLE_CHOICES, default='citoyen')
    sexe = models.CharField("Sexe", max_length=1, choices=SEXE_CHOICES, blank=True)
    date_naissance = models.DateField("Date de naissance", null=True, blank=True)
    telephone = models.CharField("Téléphone", max_length=20, blank=True)
    ville = models.CharField("Ville", max_length=100, blank=True)
    profession = models.CharField("Profession", max_length=100, blank=True)
    bio = models.TextField("Présentation", blank=True)

    photo = models.ImageField(
        "Photo",
        upload_to='citoyen_photos/',
        blank=True,
        null=True,
        help_text="Photo de profil au format carré"
    )

    created_at = models.DateTimeField("Date de création", auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.role})"

    def photo_url(self):
        try:
            return self.photo.url
        except:
            return '/static/img/default_avatar.png'

    def age(self):
        if self.date_naissance:
            today = date.today()
            return today.year - self.date_naissance.year - (
                (today.month, today.day) < (self.date_naissance.month, self.date_naissance.day)
            )
        return None

    class Meta:
        verbose_name = "Profil citoyen"
        verbose_name_plural = "Profils citoyens"


# 🧑‍⚖️ Profil professionnel pour les juristes
class JuristeProfile(models.Model):
    PROFESSION_CHOICES = [
        ('Avocat', 'Avocat'),
        ('Magistrat', 'Magistrat'),
        ('Notaire', 'Notaire'),
        ('Huissier', 'Huissier'),
    ]

    SEXE_CHOICES = (
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('A', 'Autre'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='juriste_profile'
    )

    profession = models.CharField("Profession", max_length=30, choices=PROFESSION_CHOICES)
    sexe = models.CharField("Sexe", max_length=1, choices=SEXE_CHOICES, blank=True)
    date_naissance = models.DateField("Date de naissance", null=True, blank=True)
    specialite = models.CharField("Spécialité", max_length=100, blank=True)
    ville = models.CharField("Ville", max_length=100, null=True, blank=True)
    institution = models.CharField("Institution", max_length=100, blank=True)
    bio = models.TextField("Présentation", blank=True)

    photo = models.ImageField(
        "Photo",
        upload_to='juriste_photos/',
        blank=True,
        null=True,
        help_text="Photo professionnelle au format carré idéalement"
    )

    created_at = models.DateTimeField("Date d'ajout", auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.profession})"

    def photo_url(self):
        try:
            return self.photo.url
        except:
            return '/static/img/default_avatar.png'

    def age(self):
        if self.date_naissance:
            today = date.today()
            return today.year - self.date_naissance.year - (
                (today.month, today.day) < (self.date_naissance.month, self.date_naissance.day)
            )
        return None

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            total = sum(r.rating for r in reviews)
            return round(total / reviews.count(), 1)
        return None

    class Meta:
        verbose_name = "Profil juriste"
        verbose_name_plural = "Profils juristes"


# ⭐ Avis sur les juristes
class Review(models.Model):
    juriste = models.ForeignKey(
        JuristeProfile,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='given_reviews'
    )
    rating = models.PositiveIntegerField(
        "Note",
        choices=[(i, f"{i} ⭐") for i in range(1, 6)]
    )
    comment = models.TextField("Commentaire", blank=True)
    created_at = models.DateTimeField("Date de publication", auto_now_add=True)

    def __str__(self):
        return f"Avis par {self.reviewer} - Note : {self.rating}/5"

    class Meta:
        verbose_name = "Avis"
        verbose_name_plural = "Avis sur juristes"
        ordering = ['-created_at']
