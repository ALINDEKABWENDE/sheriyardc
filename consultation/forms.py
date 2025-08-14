from django import forms
from .models import RendezVous, Question, Réponse, AppelVideo

class RendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = ['date', 'motif']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'motif': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['objet', 'contenu', 'categorie']
        widgets = {
            'objet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre ou sujet de la question'}),
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Décrivez votre question en détail'}),
            'categorie': forms.Select(attrs={'class': 'form-select'}),
        }

class RéponseForm(forms.ModelForm):
    class Meta:
        model = Réponse
        fields = ['contenu']
        widgets = {
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class AppelVideoForm(forms.ModelForm):
    class Meta:
        model = AppelVideo
        fields = ['lien', 'date']
        widgets = {
            'lien': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Lien de la réunion vidéo'}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
