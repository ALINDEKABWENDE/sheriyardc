from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.template import Template, Context
import uuid

class Document(models.Model):
    auteur = models.ForeignKey(User, verbose_name="Auteur", on_delete=models.CASCADE)
    titre = models.CharField("Titre", max_length=200)
    contenu = models.TextField("Contenu")
    date_creation = models.DateTimeField("Date de création", auto_now_add=True)

    def __str__(self):
        return self.titre

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        ordering = ['-date_creation']


class ModeleDocument(models.Model):
    nom = models.CharField("Nom du modèle", max_length=100)
    contenu = models.TextField("Contenu du modèle", help_text="Utiliser {{ nom }}, {{ date }}, etc.")
    categorie = models.CharField("Catégorie", max_length=100)
    date_ajout = models.DateField("Date d'ajout", auto_now_add=True)
    est_actif = models.BooleanField("Actif", default=True)

    def __str__(self):
        return f"{self.nom} ({self.categorie})"

    class Meta:
        verbose_name = "Modèle de document"
        verbose_name_plural = "Modèles de documents"
        ordering = ['-date_ajout']


class DocumentGenere(models.Model):  # Sans accent pour éviter les problèmes d'import
    TYPES = [
        # Juridiques
        ('contrat', 'Contrat'),
        ('statuts', 'Statuts de société'),
        ('mise_en_demeure', 'Lettre de mise en demeure'),
        ('testament', 'Testament'),
        ('procuration', 'Procuration'),
        ('affidavit', 'Affidavit'),
        ('engagement', 'Acte d’engagement'),
        ('convention', 'Convention'),
        ('declaration', 'Déclaration sur l’honneur'),

        # Administratifs et civils
        ('attestation', 'Attestation'),
        ('certificat', 'Certificat'),
        ('autorisation', 'Autorisation'),
        ('demande', 'Lettre de demande'),
        ('notification', 'Notification officielle'),
        ('reçu', 'Reçu de paiement'),
        ('passeport', 'Demande de passeport'),
        ('carte_identite', 'Demande de carte d’identité'),
        ('extrait_naissance', 'Extrait d’acte de naissance'),
        ('casier_judiciaire', 'Demande de casier judiciaire'),

        # Professionnels et institutionnels
        ('rapport', 'Rapport'),
        ('memo', 'Note ou mémo'),
        ('recommandation', 'Lettre de recommandation'),
        ('plainte', 'Plainte'),
        ('convocation', 'Convocation'),
        ('avis', 'Avis officiel'),
        ('ordre_mission', 'Ordre de mission'),

        # Autres
        ('autre', 'Autre'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    utilisateur = models.ForeignKey(User, verbose_name="Utilisateur", on_delete=models.CASCADE)
    modele = models.ForeignKey(ModeleDocument, verbose_name="Modèle utilisé", on_delete=models.SET_NULL, null=True)
    type_document = models.CharField("Type de document", max_length=50, choices=TYPES, default='autre')
    champs_remplis = models.JSONField("Champs remplis")
    pdf_fichier = models.FileField("Fichier PDF généré", upload_to="documents_generes/", blank=True, null=True)
    date_creation = models.DateTimeField("Date de génération", auto_now_add=True)
    version = models.PositiveIntegerField("Version", default=1)
    est_signe = models.BooleanField("Signé électroniquement", default=False)
    signature = models.ImageField("Signature", upload_to="signatures/", blank=True, null=True)
    qr_code = models.ImageField("QR Code", upload_to="qr_codes/", blank=True, null=True)
    slug = models.SlugField("Slug", unique=True, blank=True)

    def __str__(self):
        return f"{self.get_type_document_display()} généré par {self.utilisateur.username} le {self.date_creation.strftime('%d/%m/%Y')}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{self.type_document}-{uuid.uuid4().hex[:6]}"
        super().save(*args, **kwargs)

    def render_contenu(self):
        """Rend le contenu du modèle avec les champs remplis"""
        if self.modele and self.champs_remplis:
            template = Template(self.modele.contenu)
            context = Context(self.champs_remplis)
            return template.render(context)
        return ""

    class Meta:
        verbose_name = "Document généré"
        verbose_name_plural = "Documents générés"
        ordering = ['-date_creation']
