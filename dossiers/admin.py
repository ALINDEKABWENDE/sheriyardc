# dossiers/admin.py
from django.contrib import admin
from .models import Dossier

class DossierAdmin(admin.ModelAdmin):
    list_display = ("titre", "statut", "date_audience", "utilisateur")
    search_fields = ("titre", "statut")
    list_filter = ("statut",)

admin.site.register(Dossier, DossierAdmin)


# Register your models here.
