from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import Recommandation
from .serializers import RecommandationSerializer


class RecommandationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Lecture seule : les recommandations sont générées côté backend
    (management command / moteur de scoring), jamais créées via l'API.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = RecommandationSerializer
    http_method_names = ["get", "patch", "head", "options"]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "role", None) != "candidat":
            return Recommandation.objects.none()
        return Recommandation.objects.filter(candidat=user.candidat).select_related("offre")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.statut == Recommandation.Statut.NOUVELLE:
            instance.statut = Recommandation.Statut.VUE
            instance.date_consultation = timezone.now()
            instance.save(update_fields=["statut", "date_consultation"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"])
    def ignorer(self, request, pk=None):
        recommandation = self.get_object()
        recommandation.statut = Recommandation.Statut.IGNOREE
        recommandation.save(update_fields=["statut"])
        serializer = self.get_serializer(recommandation)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def nouvelles(self, request):
        queryset = self.get_queryset().filter(statut=Recommandation.Statut.NOUVELLE)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)