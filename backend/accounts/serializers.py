# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .models import Candidat, Recruteur, Utilisateur
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

Utilisateur = get_user_model()
token_generator = PasswordResetTokenGenerator()


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





class UtilisateurSerializer(serializers.ModelSerializer):

    password1 = serializers.CharField(
        write_only=True,
        required=True
    )

    password2 = serializers.CharField(
        write_only=True,
        required=True
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
            "password1",
            "password2",
        ]

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError({
                "password2": "Les mots de passe ne correspondent pas."
            })

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password1")
        validated_data.pop("password2")

        utilisateur = Utilisateur(**validated_data)
        utilisateur.set_password(password)
        utilisateur.save()

        return utilisateur





class CandidatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Candidat
        fields = [
            "utilisateur",
            "niveau_etude",
            "domaine_metier",
            "statut_recherche",
            "disponibilite",
            "lien_linkedin",
            "lien_porfolio",
        ]


class CandidatInscriptionSerializer(serializers.ModelSerializer):

    utilisateur = UtilisateurSerializer()

    class Meta:
        model = Candidat
        fields = [
            "utilisateur",
            "niveau_etude",
            "domaine_metier",
            "statut_recherche",
            "disponibilite",
            "lien_linkedin",
            "lien_portfolio",
        ]

    def create(self, validated_data):

        utilisateur_data = validated_data.pop("utilisateur")

        utilisateur_serializer = UtilisateurSerializer(
            data=utilisateur_data
        )

        utilisateur_serializer.is_valid(raise_exception=True)

        utilisateur = utilisateur_serializer.save()

        candidat = Candidat.objects.create(
            utilisateur=utilisateur,
            **validated_data
        )

        return candidat


class RecruteurSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recruteur
        fields = [
            "utilisateur",
            "poste",
        ]


class RecruteurInscriptionSerializer(serializers.ModelSerializer):

    utilisateur = UtilisateurSerializer()

    class Meta:
        model = Recruteur
        fields = [
            "utilisateur",
            "poste",
        ]

    def create(self, validated_data):

        utilisateur_data = validated_data.pop("utilisateur")

        utilisateur_serializer = UtilisateurSerializer(
            data=utilisateur_data
        )

        utilisateur_serializer.is_valid(raise_exception=True)

        utilisateur = utilisateur_serializer.save()

        # On force le rôle du compte à "recruteur"
        utilisateur.role = "recruteur"
        utilisateur.save()

        recruteur = Recruteur.objects.create(
            utilisateur=utilisateur,
            **validated_data
        )

        return recruteur


class ChangerMotDePasseSerializer(serializers.Serializer):

    ancien_password = serializers.CharField(
        write_only=True,
        required=True
    )

    nouveau_password1 = serializers.CharField(
        write_only=True,
        required=True
    )

    nouveau_password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    def validate(self, attrs):

        utilisateur = self.context["request"].user

        if not utilisateur.check_password(
            attrs["ancien_password"]
        ):
            raise serializers.ValidationError({
                "ancien_password": "L'ancien mot de passe est incorrect."
            })

        if attrs["nouveau_password1"] != attrs["nouveau_password2"]:
            raise serializers.ValidationError({
                "nouveau_password2":
                "Les nouveaux mots de passe ne correspondent pas."
            })

        return attrs





class DeconnexionSerializer(serializers.Serializer):

    refresh = serializers.CharField()

    def validate(self, attrs):

        try:
            token = RefreshToken(attrs["refresh"])
            token.blacklist()

        except Exception:
            raise serializers.ValidationError(
                "Le refresh token est invalide."
            )

        return attrs