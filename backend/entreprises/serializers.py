from rest_framework import serializers
from .models import Entreprise


class EntrepriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entreprise
        fields = [
            'raison_sociale',
            'logo',
            'banniere',
            'description',
            'secteur_activite',
            'taille_effectif',
            'date_creation_entreprise',
            'ninea',
            'registre_commerce',
            'email_contact',
            'telephone',
            'site_web',
            'linkedin_url',
            'adresse',
            'ville',
            'pays',
        ]