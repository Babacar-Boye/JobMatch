from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from .models import Entreprise
from .serializers import EntrepriseSerializer




# Create your views here.




class EntrepriseViewSet(viewsets.ModelViewset):
    queryset = Entreprise.objects.all()
    serializer_class = EntrepriseSerializer
    permission_classes = [permissions.IsAuthenticated]
    