# dossiers/forms.py
from django import forms
from .models import Dossier

class DossierForm(forms.ModelForm):
    class Meta:
        model = Dossier
        fields = ["titre", "description", "statut", "date_audience", "pieces_jointes"]
