from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Entretien, Evaluation, CritereEvaluation
from .serializers import (
    EntretienSerializer,
    EntretienCreateSerializer,
    EvaluationSerializer,
    CritereEvaluationSerializer,
)


class EntretienViewSet(viewsets.ModelViewSet):
    """
    CRUD complet sur Entretien, plus des actions personnalisées
    correspondant aux méthodes métier du diagramme UML.
    """

    queryset = Entretien.objects.all().order_by("-dateHeure")

    def get_serializer_class(self):
        if self.action == "create":
            return EntretienCreateSerializer
        return EntretienSerializer

    # ---- Actions métier ----

    @action(detail=True, methods=["post"])
    def confirmer(self, request, pk=None):
        """POST /entretiens/{id}/confirmer/"""
        entretien = self.get_object()
        entretien.confirmer()
        serializer = self.get_serializer(entretien)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def annuler(self, request, pk=None):
        """POST /entretiens/{id}/annuler/"""
        entretien = self.get_object()
        entretien.annuler()
        serializer = self.get_serializer(entretien)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def reprogrammer(self, request, pk=None):
        """
        POST /entretiens/{id}/reprogrammer/
        Body attendu : { "dateHeure": "2026-09-01T10:00:00Z" }
        """
        entretien = self.get_object()
        nouvelle_date = request.data.get("dateHeure")
        if not nouvelle_date:
            return Response(
                {"detail": "Le champ 'dateHeure' est requis."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        entretien.reprogrammer(nouvelle_date)
        serializer = self.get_serializer(entretien)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def envoyer_rappel(self, request, pk=None):
        """POST /entretiens/{id}/envoyer_rappel/"""
        entretien = self.get_object()
        entretien.envoyerRappel()
        serializer = self.get_serializer(entretien)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def terminer(self, request, pk=None):
        """POST /entretiens/{id}/terminer/"""
        entretien = self.get_object()
        entretien.terminer()
        serializer = self.get_serializer(entretien)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="generer-lien-visio")
    def generer_lien_visio(self, request, pk=None):
        """POST /entretiens/{id}/generer-lien-visio/"""
        entretien = self.get_object()
        lien = entretien.genererLienVisio()
        return Response({"lienVisio": lien}, status=status.HTTP_200_OK)


class EvaluationViewSet(viewsets.ModelViewSet):
    """
    CRUD complet sur Evaluation (avec critères imbriqués),
    plus des actions personnalisées pour la logique métier.
    """

    queryset = Evaluation.objects.all().order_by("-dateEvaluation")
    serializer_class = EvaluationSerializer

    @action(detail=True, methods=["post"], url_path="calculer-note-globale")
    def calculer_note_globale(self, request, pk=None):
        """POST /evaluations/{id}/calculer-note-globale/"""
        evaluation = self.get_object()
        note = evaluation.calculerNoteGlobale()
        return Response({"noteGlobale": note}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="partager-feedback")
    def partager_feedback(self, request, pk=None):
        """POST /evaluations/{id}/partager-feedback/"""
        evaluation = self.get_object()
        evaluation.partagerFeedback()
        return Response(
            {"detail": "Feedback partagé avec succès."},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="modifier-decision")
    def modifier_decision(self, request, pk=None):
        """
        POST /evaluations/{id}/modifier-decision/
        Body attendu : { "decision": "favorable" }
        """
        evaluation = self.get_object()
        nouvelle_decision = request.data.get("decision")
        if nouvelle_decision not in dict(Evaluation.DECISION_CHOICES):
            return Response(
                {"detail": "Valeur de 'decision' invalide."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        evaluation.modifierDecision(nouvelle_decision)
        serializer = self.get_serializer(evaluation)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CritereEvaluationViewSet(viewsets.ModelViewSet):
    """
    CRUD complet sur CritereEvaluation.
    Peut être filtré par évaluation via ?evaluation=<id>.
    """

    queryset = CritereEvaluation.objects.all()
    serializer_class = CritereEvaluationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        evaluation_id = self.request.query_params.get("evaluation")
        if evaluation_id:
            queryset = queryset.filter(evaluation_id=evaluation_id)
        return queryset

    @action(detail=True, methods=["post"])
    def valider(self, request, pk=None):
        """POST /criteres-evaluation/{id}/valider/"""
        critere = self.get_object()
        try:
            critere.valider()
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(critere)
        return Response(serializer.data, status=status.HTTP_200_OK)