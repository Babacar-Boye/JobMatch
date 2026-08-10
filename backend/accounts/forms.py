from django import forms
from .models import Utilisateur, Recruteur, Administrateur
from django.utils import timezone

class UtilisateurForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Mot de passe",
        min_length = 8,
        widget = forms.PasswordInput(attrs={"class": "form-control"}),
    )

    password2 = forms.CharField(
        label="Confirmer le mot de passe",
        min_length = 8,
        widget = forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Utilisateur

        fields = [
            "nom",
            "prenom",
            "nom_utilisateur",
            "email",
            "telephone",
            "date_naissance",
            "photo_profil",
        ]

        widgets = {
            "nom": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Entrez votre nom"
            }),

            "prenom": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Entrez votre prénom"
            }),

            "nom_utilisateur": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Choisissez un nom d'utilisateur"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "exemple@gmail.com"
            }),

            "telephone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "+221 77 123 45 67"
            }),

            "date_naissance": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "photo_profil": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
        }

        labels = {
            "nom": "Nom",
            "prenom": "Prénom",
            "nom_utilisateur": "Nom d'utilisateur",
            "email": "Adresse e-mail",
            "telephone": "Téléphone",
            "date_naissance": "Date de naissance",
            "photo_profil": "Photo de profil",
        }

        help_texts = {
            "nom_utilisateur": "Ce nom sera utilisé pour vous identifier.",
            "telephone": "Champ facultatif.",
            "photo_profil": "Formats acceptés : JPG, JPEG ou PNG."
        }

        error_messages = {
            "nom": {
                "required": "Le nom est obligatoire."
            },
            "prenom": {
                "required": "Le prénom est obligatoire."
            },
            "nom_utilisateur": {
                "required": "Le nom d'utilisateur est obligatoire.",
                "unique": "Ce nom d'utilisateur est déjà utilisé."
            },
            "email": {
                "required": "L'adresse e-mail est obligatoire.",
                "unique": "Cette adresse e-mail est déjà utilisée."
            },
            "telephone": {
                "unique": "Ce numéro de téléphone est déjà utilisé."
            }
        }

    def clean(self):
        cleanead = super().clean()
        mdp1 = cleanead.get('password1')
        mdp2 = cleanead.get('password2')

        if mdp1 and mdp2 and mdp1 != mdp2 :
            raise forms.validationError('Les mots de passe ne correspondent pas!')
        return cleanead

    def save(self, commit = True):
        utilisateur = super().save(commit = False)

        utilisateur.set_password(
            self.cleaned_data["password1"]
        )

        if commit:
            utilisateur.save()

        return utilisateur







class CandidatForm(forms.ModelForm):

    class Meta:
        model = Candidat

        fields = [
            "niveau_etude",
            "domaine_metier",
            "statut_recherche",
            "disponibilite",
            "lien_linkedin",
            "lien_portfolio",
        ]

        widgets = {
            "niveau_etude": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "domaine_metier": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "statut_recherche": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

            "disponibilite": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
        }

    def clean_disponibilite(self):
        disponibilite = self.cleaned_data.get("disponibilite")

        if disponibilite and disponibilite < timezone.localdate():
            raise forms.ValidationError(
                "La date de disponibilité ne peut pas être dans le passé."
            )

        return disponibilite

    def clean(self):
        cleaned_data = super().clean()

        statut_recherche = cleaned_data.get("statut_recherche")
        disponibilite = cleaned_data.get("disponibilite")

        if not statut_recherche and disponibilite:
            self.add_error(
                "disponibilite",
                "Vous ne pouvez pas renseigner une date de disponibilité "
                "si vous ne recherchez pas actuellement un emploi."
            )

        return cleaned_data



class RecruteurForm(forms.ModelForm):

    class Meta:
        model = Recruteur

        fields = [
            "poste",
        ]

        widgets = {
            "poste": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Votre poste dans l'entreprise"
            }),
        }

        labels = {
            "poste": "Poste occupé",
        }

        error_messages = {
            "poste": {
                "required": "Le poste est obligatoire."
            }
        }