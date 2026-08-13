from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Candidat, Recruteur
from .permissions import IsAdministrateur
from .serializers import (
    UtilisateurProfilSerializer,
    CandidatSerializer, CandidatInscriptionSerializer,
    RecruteurSerializer, RecruteurInscriptionSerializer,
    ChangerMotDePasseSerializer, ConnexionSerializer, DeconnexionSerializer,
    DemandeReinitialisationSerializer, ConfirmerReinitialisationSerializer,
)

Utilisateur = get_user_model()
token_generator_reset = PasswordResetTokenGenerator()


def _envoyer_email_verification(request, utilisateur):
    uid = urlsafe_base64_encode(force_bytes(utilisateur.pk))
    token = default_token_generator.make_token(utilisateur)
    lien = f"{settings.FRONTEND_URL}/verifier-email/{uid}/{token}/"

    send_mail(
        subject="Vérifiez votre compte JobMatch AI",
        message=f"Bonjour {utilisateur.prenom},\n\nCliquez sur ce lien pour activer votre compte :\n{lien}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[utilisateur.email],
    )


# ─────────────────────────────
# AUTH — connexion / déconnexion / vérification email (JWT)
# ─────────────────────────────

class AuthViewSet(viewsets.ViewSet):

    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny], url_path="connexion")
    def connexion(self, request):
        serializer = ConnexionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        utilisateur = serializer.validated_data["utilisateur"]

        refresh = RefreshToken.for_user(utilisateur)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "utilisateur": UtilisateurProfilSerializer(utilisateur).data,
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated], url_path="deconnexion")
    def deconnexion(self, request):
        serializer = DeconnexionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # blackliste le refresh token
        return Response({"message": "Déconnexion réussie."}, status=status.HTTP_205_RESET_CONTENT)

    @action(
        detail=False, methods=["get"], permission_classes=[permissions.AllowAny],
        url_path=r"verifier-email/(?P<uid>[^/.]+)/(?P<token>[^/.]+)"
    )
    def verifier_email(self, request, uid, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            utilisateur = Utilisateur.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, Utilisateur.DoesNotExist):
            return Response({"message": "Lien de vérification invalide."}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(utilisateur, token):
            return Response({"message": "Lien de vérification invalide ou expiré."}, status=status.HTTP_400_BAD_REQUEST)

        utilisateur.email_verifie = True

        # Un candidat devient actif direct ; un recruteur attend en plus la validation admin
        if utilisateur.role == "candidat":
            utilisateur.is_active = True

        utilisateur.save()

        return Response({"message": "Email vérifié avec succès."}, status=status.HTTP_200_OK)


# ─────────────────────────────
# UTILISATEUR — actions liées uniquement à SON PROPRE compte
# (pas de ModelViewSet ici : aucune route list/retrieve/update/destroy
# générique par id, pour éviter qu'un utilisateur accède au compte d'un autre)
# ─────────────────────────────

class UtilisateurViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="profil")
    def profil(self, request):
        return Response(UtilisateurProfilSerializer(request.user).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["patch"], url_path="modifier-profil")
    def modifier_profil(self, request):
        serializer = UtilisateurProfilSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="modifier-password")
    def modifier_password(self, request):
        serializer = ChangerMotDePasseSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        request.user.set_password(serializer.validated_data["nouveau_password1"])
        request.user.save()

        return Response({"message": "Votre mot de passe a été modifié avec succès."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="desactiver")
    def desactiver(self, request):
        utilisateur = request.user
        utilisateur.statut_compte = "desactive_utilisateur"
        utilisateur.is_active = False
        utilisateur.save()
        return Response({"message": "Votre compte a été désactivé."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"], url_path="supprimer")
    def supprimer(self, request):
        password = request.data.get("password")
        if not password:
            return Response({"password": "Le mot de passe est obligatoire."}, status=status.HTTP_400_BAD_REQUEST)

        utilisateur = request.user
        if not utilisateur.check_password(password):
            return Response({"password": "Mot de passe incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        utilisateur.statut_compte = "supprime"
        utilisateur.is_active = False
        utilisateur.email = f"supprime_{utilisateur.pk}@jobmatch.ai"
        utilisateur.save()

        return Response({"message": "Votre compte a été supprimé."}, status=status.HTTP_200_OK)


# ─────────────────────────────
# CANDIDAT
# ─────────────────────────────

class CandidatViewSet(viewsets.ModelViewSet):
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return CandidatInscriptionSerializer
        return CandidatSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [IsAdministrateur()]  # le candidat gère son propre profil via /utilisateurs/modifier-profil/

    def perform_create(self, serializer):
        self._candidat_cree = serializer.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        _envoyer_email_verification(request, self._candidat_cree.utilisateur)
        response.data = {"message": "Compte créé. Vérifiez votre email pour l'activer."}
        return response


# ─────────────────────────────
# RECRUTEUR
# ─────────────────────────────

class RecruteurViewSet(viewsets.ModelViewSet):
    queryset = Recruteur.objects.all()
    serializer_class = RecruteurSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return RecruteurInscriptionSerializer
        return RecruteurSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [IsAdministrateur()]

    def perform_create(self, serializer):
        self._recruteur_cree = serializer.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        _envoyer_email_verification(request, self._recruteur_cree.utilisateur)
        response.data = {"message": "Compte créé. Vérifiez votre email, puis attendez la validation admin."}
        return response

    @action(detail=False, methods=["get"], permission_classes=[IsAdministrateur], url_path="en-attente")
    def en_attente(self, request):
        recruteurs = Recruteur.objects.filter(utilisateur__email_verifie=True, compte_valide=False)
        return Response(RecruteurSerializer(recruteurs, many=True).data)

    @action(detail=True, methods=["post"], permission_classes=[IsAdministrateur], url_path="valider")
    def valider(self, request, pk=None):
        recruteur = self.get_object()
        recruteur.compte_valide = True
        recruteur.save()

        utilisateur = recruteur.utilisateur
        utilisateur.is_active = True
        utilisateur.save()

        return Response({"message": "Compte recruteur validé."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["delete"], permission_classes=[IsAdministrateur], url_path="refuser")
    def refuser(self, request, pk=None):
        recruteur = self.get_object()
        recruteur.utilisateur.delete()
        return Response({"message": "Demande recruteur refusée."}, status=status.HTTP_204_NO_CONTENT)


# ─────────────────────────────
# RESET PASSWORD ("mot de passe oublié")
# ─────────────────────────────

class DemandeReinitialisationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = DemandeReinitialisationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = Utilisateur.objects.get(email__iexact=email, is_active=True)
        except Utilisateur.DoesNotExist:
            return Response(
                {"detail": "Si ce compte existe, un email de réinitialisation a été envoyé."},
                status=status.HTTP_200_OK
            )

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator_reset.make_token(user)
        lien = f"{settings.FRONTEND_URL}/reinitialiser-mot-de-passe/{uid}/{token}/"

        message = render_to_string('emails/password_reset_email.txt', {'user': user, 'lien': lien})

        send_mail(
            subject="Réinitialisation de votre mot de passe - JobMatch AI",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        return Response(
            {"detail": "Si ce compte existe, un email de réinitialisation a été envoyé."},
            status=status.HTTP_200_OK
        )


class ConfirmerReinitialisationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ConfirmerReinitialisationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        user.set_password(serializer.validated_data['nouveau_mot_de_passe'])
        user.save()

        return Response({"detail": "Mot de passe réinitialisé avec succès."}, status=status.HTTP_200_OK)