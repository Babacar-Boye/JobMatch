from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from .models import OffreEmploi, CompetenceRequise
from . serializers import ( 
                           OffreEmploiCreateUpdateSerializer, 
                           OffreEmploi, OffreEmploiDetailSerializer, 
                           OffreEmploiListSerializer)

# Create your views here.


class OffreEmploiListViewSet(viewsets.ModelViewSet):
    queryset = OffreEmploi.objects.all()
    serializers = OffreEmploiListSerializer()
    
    
class OffreEmploiDetailViewSet(viewsets.MOdelViewSet):
    queryset = OffreEmploi.objects.all()
    serializers_class =  OffreEmploiDetailSerializer
    
    

class OffreEmploiCreateUpdateViewSet(viewsets.ModelViewSet):
    queryset = OffreEmploi.objects.all()
    serializers_class =  OffreEmploiCreateUpdateSerializer