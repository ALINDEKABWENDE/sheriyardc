from django import forms
from django.contrib.auth.models import User
from accounts.models import UserProfile

class CitoyenSignupForm(forms.ModelForm):
    full_name = forms.CharField(label="Nom complet", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    sexe = forms.ChoiceField(choices=UserProfile.SEXE_CHOICES, label="Sexe")
    date_naissance = forms.DateField(label="Date de naissance", required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    ville = forms.CharField(label="Ville", required=False)
    profession = forms.CharField(label="Profession", required=False)
    telephone = forms.CharField(label="Téléphone", required=False)
    bio = forms.CharField(label="Présentation", widget=forms.Textarea, required=False)
    photo = forms.ImageField(label="Photo de profil", required=False)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password']
        labels = {
            'email': 'Adresse email',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

    def save(self, commit=True):
        # Crée l'utilisateur
        user = User()
        full_name = self.cleaned_data['full_name']
        parts = full_name.split()
        user.first_name = parts[0]
        user.last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
        user.username = full_name  # ou un slug si tu veux éviter les doublons
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

            # Crée le profil citoyen
            UserProfile.objects.create(
                user=user,
                role='citoyen',
                sexe=self.cleaned_data['sexe'],
                date_naissance=self.cleaned_data['date_naissance'],
                ville=self.cleaned_data['ville'],
                profession=self.cleaned_data['profession'],
                telephone=self.cleaned_data['telephone'],
                bio=self.cleaned_data['bio'],
                photo=self.cleaned_data.get('photo')
            )

        return user
