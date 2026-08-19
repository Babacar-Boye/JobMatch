from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Utilisateur, Candidat, Recruteur

Utilisateur = get_user_model()
token_generator = PasswordResetTokenGenerator()


# ─────────────────────────────
# RESET PASSWORD ("mot de passe oublié")
# ─────────────────────────────

class DemandeReinitialisationSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ConfirmerReinitialisationSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    nouveau_mot_de_passe = serializers.CharField(min_length=8, write_only=True)

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(data['uid']))
            user = Utilisateur.objects.get(pk=uid)
        except (Utilisateur.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError("Lien de réinitialisation invalide.")

        if not token_generator.check_token(user, data['token']):
            raise serializers.ValidationError("Ce lien a expiré ou a déjà été utilisé.")

        data['user'] = user
        return data


# ─────────────────────────────
# UTILISATEUR
# ─────────────────────────────

class UtilisateurInscriptionSerializer(serializers.ModelSerializer):
    """Usage interne uniquement, appelé par CandidatInscriptionSerializer /
    RecruteurInscriptionSerializer. Ne jamais l'exposer seul en API publique."""

    password1 = serializers.CharField(write_only=True, required=True, min_length=8)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Utilisateur
        fields = [
            "nom", "prenom", "nom_utilisateur", "email", "telephone",
            "date_naissance", "photo_profil", "password1", "password2",
        ]

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError({"password2": "Les mots de passe ne correspondent pas."})
        return attrs

    def validate_email(self, value):
        if Utilisateur.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password1")

        # Toujours inactif à la création : activation via vérification email (+ validation admin pour recruteur)
        utilisateur = Utilisateur(**validated_data, is_active=False, email_verifie=False)
        utilisateur.set_password(password)
        utilisateur.save()
        return utilisateur


class UtilisateurProfilSerializer(serializers.ModelSerializer):
    """Pour consulter / modifier son propre profil. Email, rôle et statut non modifiables ici."""

    class Meta:
        model = Utilisateur
        fields = [
            "id", "nom", "prenom", "nom_utilisateur", "email", "telephone",
            "date_naissance", "role", "photo_profil", "date_incription",
            "statut_compte", "email_verifie",
        ]
        read_only_fields = ["id", "email", "role", "date_incription", "statut_compte", "email_verifie"]


# ─────────────────────────────
# CANDIDAT
# ─────────────────────────────

class CandidatSerializer(serializers.ModelSerializer):
    utilisateur = UtilisateurProfilSerializer(read_only=True)

    class Meta:
        model = Candidat
        fields = [
            "id", "utilisateur", "niveau_etude", "domaine_metier",
            "statut_recherche", "disponibilite", "lien_linkedin", "lien_portfolio",
        ]


class CandidatInscriptionSerializer(serializers.ModelSerializer):
    utilisateur = UtilisateurInscriptionSerializer()

    class Meta:
        model = Candidat
        fields = [
            "utilisateur", "niveau_etude", "domaine_metier",
            "statut_recherche", "disponibilite", "lien_linkedin", "lien_portfolio",
        ]

    def create(self, validated_data):
        utilisateur_data = validated_data.pop("utilisateur")

        utilisateur_serializer = UtilisateurInscriptionSerializer(data=utilisateur_data)
        utilisateur_serializer.is_valid(raise_exception=True)
        utilisateur = utilisateur_serializer.save()

        utilisateur.role = "candidat"
        utilisateur.save()

        return Candidat.objects.create(utilisateur=utilisateur, **validated_data)


# ─────────────────────────────
# RECRUTEUR
# ─────────────────────────────

class RecruteurSerializer(serializers.ModelSerializer):
    utilisateur = UtilisateurProfilSerializer(read_only=True)

    class Meta:
        model = Recruteur
        fields = ["id", "utilisateur", "poste", "compte_valide"]


class RecruteurInscriptionSerializer(serializers.ModelSerializer):
    utilisateur = UtilisateurInscriptionSerializer()

    class Meta:
        model = Recruteur
        fields = ["utilisateur", "poste"]

    def create(self, validated_data):
        utilisateur_data = validated_data.pop("utilisateur")

        utilisateur_serializer = UtilisateurInscriptionSerializer(data=utilisateur_data)
        utilisateur_serializer.is_valid(raise_exception=True)
        utilisateur = utilisateur_serializer.save()

        utilisateur.role = "recruteur"
        utilisateur.save()

        # compte_valide=False par défaut → nécessite validation admin en plus de l'email
        return Recruteur.objects.create(utilisateur=utilisateur, **validated_data)


# ─────────────────────────────
# CONNEXION / DÉCONNEXION (JWT)
# ─────────────────────────────

class ConnexionSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # authenticate() attend "username" même si USERNAME_FIELD = "email"
        utilisateur = authenticate(username=data["email"], password=data["password"])

        if utilisateur is None:
            raise serializers.ValidationError("Email ou mot de passe incorrect.")

        if not utilisateur.is_active:
            raise serializers.ValidationError("Ce compte n'est pas encore actif.")

        data["utilisateur"] = utilisateur
        return data


class DeconnexionSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        try:
            token = RefreshToken(attrs["refresh"])
            token.blacklist()
        except Exception:
            raise serializers.ValidationError("Le refresh token est invalide.")
        return attrs


# ─────────────────────────────
# MOT DE PASSE (utilisateur connecté)
# ─────────────────────────────

class ChangerMotDePasseSerializer(serializers.Serializer):
    ancien_password = serializers.CharField(write_only=True, required=True)
    nouveau_password1 = serializers.CharField(write_only=True, required=True, min_length=8)
    nouveau_password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        utilisateur = self.context["request"].user

        if not utilisateur.check_password(attrs["ancien_password"]):
            raise serializers.ValidationError({"ancien_password": "L'ancien mot de passe est incorrect."})

        if attrs["nouveau_password1"] != attrs["nouveau_password2"]:
            raise serializers.ValidationError({"nouveau_password2": "Les nouveaux mots de passe ne correspondent pas."})

        return attrs