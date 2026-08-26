from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from .models import Entreprise
from .serializers import EntrepriseSerializer, EntreprisePublicSerializer




# Create your views here.




class EntrepriseViewSet(viewsets.ModelViewSet):
    
    queryset = Entreprise.objects.all()
    serializer_class = EntrepriseSerializer
    # permission_classes = [permissions.IsAuthenticated]
    
    # def get_queryset(self):
    #     return Entreprise.objects.filter(recruteur = self.request.user.recruteur)
    
    
class EnrteprisePublicViewSet(viewsets.ModelViewSet):
    queryset = Entreprise.objects.filter(est_active=True)
    serializer_class = EntreprisePublicSerializer
    # permission_classes = [permissions.IsAuthenticated]