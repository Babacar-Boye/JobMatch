from rest_framework import serializers
from .models import Entreprise


class EntrepriseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Entreprise
        fields = [
            "id",
            "raison_sociale",
            "logo",
            "banniere",
            "description",
            "secteur_activite",
            "taille_effectif",
            "date_creation_entreprise",
            "ninea",
            "registre_commerce",
            "email_contact",
            "telephone",
            "site_web",
            "linkedin_url",
            "adresse",
            "ville",
            "pays",
            "statut_verification",
            "date_verification",
            "est_active",
            "date_creation",
            "date_modification",
        ]
        read_only_fields = [
            "id",
            "statut_verification",   # décidé par un admin, pas par le recruteur lui-même
            "date_verification",     # idem
            "est_active",            # idem — sinon un recruteur pourrait se "réactiver" après suspension
            "date_creation",
            "date_modification",
        ]
        
        
class EntreprisePublicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Entreprise
        fields = [
            "id",
            "raison_sociale",
            "logo",
            "banniere",
            "description",
            "secteur_activite",
            "taille_effectif",
            "site_web",
            "linkedin_url",
            "ville",
            "pays",
            "statut_verification",   # utile à afficher (badge "vérifiée") mais...
        ]
        read_only_fields = fields  # tout est en lecture seule ici, ce serializer ne sert jamais à écrire