from django.shortcuts import render
from .forms import UtilisateurForm, CandidatForm
from django.shortcuts import render, redirect

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from .serializers import DemandeReinitialisationSerializer, ConfirmerReinitialisationSerializer

from django.contrib.auth.tokens import default_token_generator

from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings


from rest_framework import viewsets
from rest_framework.decorators import action


from django.utils.http import (
    urlsafe_base64_decode
)


# Create your views here.


from .models import Utilisateur, Candidat, Recruteur
from .serializers import UtilisateurSerializer, CandidatSerializer, RecruteurInscriptionSerializer, RecruteurSerializer



from rest_framework.permissions import IsAuthenticated


class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer

class CandidatViewSet(viewsets.ModelViewSet):
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return CandidatInscriptionSerializer

        return CandidatSerializer

class RecruteurViewSet(viewsets.ModelViewSet):

    queryset = Recruteur.objects.all()

    serializer_class = RecruteurSerializer

    def get_serializer_class(self):

        if self.action == "create":
            return RecruteurInscriptionSerializer

        return RecruteurSerializer

# def modifier_utilisateur(request, pk):
#     utilisateur = get_object_or_404(Utilisateur, pk = pk)

#     form_utilisateur = UtilisateurForm(request.POST or None, request.FILES or None, instance = utilisateur)

#     if form_utilisateur.is_valid():
#         form_utilisateur.save()
#         return redirect('profil_utilisateur')

#     return render(request, 'modifier_profil.html', {'form_utilisateur': form_utilisateur})



class UtilisateurViewSet(viewsets.ModelViewSet):

    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        url_path="modifier-password"
    )
    def modifier_password(self, request):

        serializer = ChangerMotDePasseSerializer(
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        utilisateur = request.user

        utilisateur.set_password(
            serializer.validated_data["nouveau_password1"]
        )

        utilisateur.save()

        return Response(
            {
                "message":
                "Votre mot de passe a été modifié avec succès."
            },
            status=status.HTTP_200_OK
        )
    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="profil"
    )
    def profil(self, request):

        serializer = UtilisateurSerializer(
            request.user
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        url_path="desactiver"
    )
    def desactiver(self, request):

        utilisateur = request.user

        utilisateur.statut_compte = "desactive_utilisateur"
        utilisateur.is_active = False
        utilisateur.save()

        logout(request)

        return Response(
            {
                "message": "Votre compte a été désactivé."
            },
            status=status.HTTP_200_OK
        )    
    

    @action(
        detail=False,
        methods=["delete"],
        permission_classes=[IsAuthenticated],
        url_path="supprimer"
    )
    def supprimer(self, request):

        utilisateur = request.user

        password = request.data.get("password")

        if not password:
            return Response(
                {
                    "password":
                    "Le mot de passe est obligatoire."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not utilisateur.check_password(password):
            return Response(
                {
                    "password":
                    "Mot de passe incorrect."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        utilisateur.statut_compte = "supprime"
        utilisateur.is_active = False
        utilisateur.email = (
            f"supprime_{utilisateur.pk}@jobmatch.ai"
        )

        utilisateur.save()

        logout(request)

        return Response(
            {
                "message": "Votre compte a été supprimé."
            },
            status=status.HTTP_200_OK
        )


class AuthViewSet(viewsets.ViewSet):

    @action(
        detail=False,
        methods=["post"],
        url_path="connexion"
    )
    # def connexion(self, request):

    #     serializer = ConnexionSerializer(
    #         data=request.data,
    #         context={"request": request}
    #     )

    #     serializer.is_valid(raise_exception=True)

    #     utilisateur = serializer.validated_data["utilisateur"]

    #     login(request, utilisateur)

    #     return Response(
    #         {
    #             "message": "Connexion réussie.",
    #             "utilisateur": utilisateur.id
    #         },
    #         status=status.HTTP_200_OK
    #     )
    @action(
        detail=False,
        methods=["post"],
        url_path="deconnexion"
    )
    def deconnexion(self, request):

        logout(request)

        return Response(
            {
                "message": "Déconnexion réussie."
            },
            status=status.HTTP_200_OK
        )

    #@action(
    #     detail=False,
    #     methods=["get"],
    #     url_path=r"verifier-email/(?P<uid>[^/.]+)/(?P<token>[^/.]+)"
    # )
    # def verifier_email(self, request, uid, token):

    #     try:

    #         user_id = force_str(
    #             urlsafe_base64_decode(uid)
    #         )

    #         utilisateur = Utilisateur.objects.get(
    #             pk=user_id
    #         )

    #     except (
    #         TypeError,
    #         ValueError,
    #         OverflowError,
    #         Utilisateur.DoesNotExist
    #     ):

    #         return Response(
    #             {
    #                 "message":
    #                 "Lien de vérification invalide."
    #             },
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    #     if not default_token_generator.check_token(
    #         utilisateur,
    #         token
    #     ):

    #         return Response(
    #             {
    #                 "message":
    #                 "Lien de vérification invalide ou expiré."
    #             },
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    #     utilisateur.email_verifie = True

    #     if utilisateur.role == "candidat":
    #         utilisateur.is_active = True

    #     utilisateur.save()

    #     return Response(
    #         {
    #             "message":
    #             "Email vérifié avec succès."
    #         },
    #         status=status.HTTP_200_OK
    #     )



class DeconnexionView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = DeconnexionSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        return Response(
            {
                "message": "Déconnexion réussie."
            },
            status=status.HTTP_200_OK
        )

Utilisateur = get_user_model()
token_generator = PasswordResetTokenGenerator()


def envoyer_email_verification(request, utilisateur):
    uid = urlsafe_base64_encode(force_bytes(utilisateur.pk))
    token = default_token_generator.make_token(utilisateur)

    lien = request.build_absolute_uri(f'/accounts/verifier-email/{uid}/{token}/')

    send_mail(
        subject="Vérifiez votre compte JobMatch AI",
        message=f"Bonjour {utilisateur.prenom},\n\nCliquez sur ce lien pour activer votre compte :\n{lien}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[utilisateur.email],
    )


# def verifier_email(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         utilisateur = Utilisateur.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, Utilisateur.DoesNotExist):
#         utilisateur = None

#     if utilisateur is not None and default_token_generator.check_token(utilisateur, token):
#         utilisateur.email_verifie = True

#         # Un candidat devient actif direct, un recruteur attend la validation admin
#         if utilisateur.role == 'candidat':
#             utilisateur.is_active = True

#         utilisateur.save()
#         messages.success(request, "Email vérifié avec succès.")
#     else:
#         messages.error(request, "Lien de vérification invalide ou expiré.")

#     return redirect('connexion')


from django.contrib.auth.decorators import user_passes_test

def admin_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.role == 'administrateur',
        login_url='connexion'
    )(view_func)


    return redirect('liste_recruteurs_en_attente')



from rest_framework.permissions import IsAuthenticated


class RecruteurViewSet(viewsets.ModelViewSet):

    queryset = Recruteur.objects.all()
    serializer_class = RecruteurSerializer

    def get_serializer_class(self):

        if self.action == "create":
            return RecruteurInscriptionSerializer

        return RecruteurSerializer

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="en-attente"
    )
    def en_attente(self, request):

        if request.user.role != "administrateur":
            return Response(
                {
                    "message":
                    "Vous n'avez pas les permissions."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        recruteurs = Recruteur.objects.filter(
            utilisateur__email_verifie=True,
            compte_valide=False
        )

        serializer = RecruteurSerializer(
            recruteurs,
            many=True
        )

        return Response(serializer.data)
    
    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        url_path="valider"
    )
    def valider(self, request, pk=None):

        if request.user.role != "administrateur":
            return Response(
                {
                    "message":
                    "Vous n'avez pas les permissions."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        recruteur = self.get_object()

        recruteur.compte_valide = True
        recruteur.save()

        utilisateur = recruteur.utilisateur
        utilisateur.is_active = True
        utilisateur.save()

        return Response(
            {
                "message":
                "Compte recruteur validé."
            },
            status=status.HTTP_200_OK
        )

    @action(
        detail=True,
        methods=["delete"],
        permission_classes=[IsAuthenticated],
        url_path="refuser"
    )
    def refuser(self, request, pk=None):

        if request.user.role != "administrateur":
            return Response(
                {
                    "message":
                    "Vous n'avez pas les permissions."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        recruteur = self.get_object()

        utilisateur = recruteur.utilisateur

        utilisateur.delete()

        return Response(
            {
                "message":
                "Demande recruteur refusée."
            },
            status=status.HTTP_204_NO_CONTENT
        )



class DemandeReinitialisationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = DemandeReinitialisationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        # Réponse volontairement identique que le compte existe ou non
        # (évite de révéler quels emails sont enregistrés)
        try:
            user = Utilisateur.objects.get(email__iexact=email, is_active=True)
        except Utilisateur.DoesNotExist:
            return Response(
                {"detail": "Si ce compte existe, un email de réinitialisation a été envoyé."},
                status=status.HTTP_200_OK
            )

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        lien = f"{settings.FRONTEND_URL}/reinitialiser-mot-de-passe/{uid}/{token}/"

        message = render_to_string('emails/password_reset_email.txt', {
            'user': user,
            'lien': lien,
        })

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

        return Response(
            {"detail": "Mot de passe réinitialisé avec succès."},
            status=status.HTTP_200_OK
        )