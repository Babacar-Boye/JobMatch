from rest_framework import viewsets, permissions

from .models import CV, Experience, Competence, Formation, Preference
from .serializers import (
    CVSerializer, ExperienceSerializer, CompetenceSerializer,
    FormationSerializer, PreferenceSerializer,
)


class CVViewSet(viewsets.ModelViewSet):
    serializer_class = CVSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CV.objects.filter(candidat=self.request.user.candidat)

    def perform_create(self, serializer):
        serializer.save(candidat=self.request.user.candidat)


class ExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Experience.objects.filter(cv__candidat=self.request.user.candidat)


class CompetenceViewSet(viewsets.ModelViewSet):
    serializer_class = CompetenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Competence.objects.filter(cv__candidat=self.request.user.candidat)


class FormationViewSet(viewsets.ModelViewSet):
    serializer_class = FormationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Formation.objects.filter(cv__candidat=self.request.user.candidat)


class PreferenceViewSet(viewsets.ModelViewSet):
    serializer_class = PreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Preference.objects.filter(candidat=self.request.user.candidat)

    def perform_create(self, serializer):
        serializer.save(candidat=self.request.user.candidat)