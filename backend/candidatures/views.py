from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from .models import Candidature, PieceJointe
from .serializers import (
    CandidatureCreateSerializer,
    CandidatureCandidatSerializer,
    CandidatureRecruteurSerializer,
    PieceJointeSerializer,
)

# Create your views here.

class IsCandidat(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and getattr(request.user, "role", None) == "candidat"


class IsRecruteur(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and getattr(request.user, "role", None) == "recruteur"


class CandidatureViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get", "post", "patch", "head", "options"]

    def get_serializer_class(self):
        if self.action == "create":
            return CandidatureCreateSerializer
        if getattr(self.request.user, "role", None) == "recruteur":
            return CandidatureRecruteurSerializer
        return CandidatureCandidatSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "role", None) == "recruteur":
            return Candidature.objects.filter(offre__recruteur=user.recruteur)
        return Candidature.objects.filter(candidat=user.candidat)

    def create(self, request, *args, **kwargs):
        if getattr(request.user, "role", None) != "candidat":
            return Response(
                {"detail": "Seul un candidat peut postuler."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        try:
            candidature = serializer.save()
        except IntegrityError:
            return Response(
                {"detail": "Vous avez déjà postulé à cette offre."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        output = CandidatureCandidatSerializer(candidature)
        return Response(output.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        candidature = self.get_object()
        if getattr(request.user, "role", None) != "recruteur":
            return Response(
                {"detail": "Seul un recruteur peut modifier une candidature."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.get_serializer(candidature, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=["patch"], permission_classes=[IsAuthenticated])
    def retirer(self, request, pk=None):
        candidature = self.get_object()
        if candidature.candidat != request.user.candidat:
            return Response(
                {"detail": "Vous ne pouvez retirer que vos propres candidatures."},
                status=status.HTTP_403_FORBIDDEN,
            )
        candidature.statut = Candidature.Statut.RETIREE
        candidature.save(update_fields=["statut"])
        serializer = CandidatureCandidatSerializer(candidature)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"], permission_classes=[IsAuthenticated])
    def changer_statut(self, request, pk=None):
        candidature = self.get_object()
        if getattr(request.user, "role", None) != "recruteur":
            return Response(
                {"detail": "Seul un recruteur peut changer le statut."},
                status=status.HTTP_403_FORBIDDEN,
            )
        nouveau_statut = request.data.get("statut")
        if nouveau_statut not in Candidature.Statut.values:
            return Response(
                {"detail": "Statut invalide."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        candidature.statut = nouveau_statut
        candidature.save(update_fields=["statut"])
        serializer = CandidatureRecruteurSerializer(candidature)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"], permission_classes=[IsAuthenticated])
    def toggle_favorite(self, request, pk=None):
        candidature = self.get_object()
        if getattr(request.user, "role", None) != "recruteur":
            return Response(
                {"detail": "Seul un recruteur peut marquer une candidature comme favorite."},
                status=status.HTTP_403_FORBIDDEN,
            )
        candidature.est_favorite = not candidature.est_favorite
        candidature.save(update_fields=["est_favorite"])
        serializer = CandidatureRecruteurSerializer(candidature)
        return Response(serializer.data)


class PieceJointeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = PieceJointeSerializer
    http_method_names = ["get", "post", "delete", "head", "options"]

    def get_queryset(self):
        user = self.request.user
        candidature_pk = self.kwargs.get("candidature_pk")
        if getattr(user, "role", None) == "recruteur":
            return PieceJointe.objects.filter(
                candidature_id=candidature_pk, candidature__offre__recruteur=user.recruteur
            )
        return PieceJointe.objects.filter(
            candidature_id=candidature_pk, candidature__candidat=user.candidat
        )

    def perform_create(self, serializer):
        candidature = get_object_or_404(
            Candidature,
            pk=self.kwargs["candidature_pk"],
            candidat=self.request.user.candidat,
        )
        fichier = self.request.data.get("fichier")
        serializer.save(
            candidature=candidature,
            nom_fichier_original=fichier.name,
            taille_fichier=fichier.size,
        )

    def perform_destroy(self, instance):
        if instance.candidature.candidat != self.request.user.candidat:
            raise PermissionError("Vous ne pouvez supprimer que vos propres pièces jointes.")
        instance.delete()