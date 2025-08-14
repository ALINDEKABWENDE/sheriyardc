from django import forms
from .models import DocumentGeneré

class DocumentForm(forms.ModelForm):
    class Meta:
        model = DocumentGeneré
        fields = ['fichier', 'titre', 'description']  # adapte selon tes champs
