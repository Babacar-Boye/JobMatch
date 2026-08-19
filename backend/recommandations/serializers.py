from rest_framework import serializers
from .models import Recommandation


class OffreRecommandeeSerializer(serializers.Serializer):
    """Aperçu minimal de l'offre liée à une recommandation.
    Adapte/complète les champs selon ceux réels de ton modèle OffreEmploi."""
    id = serializers.IntegerField()
    titre = serializers.CharField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Ajoute ici d'autres champs si besoin, ex:
        # data["entreprise"] = getattr(instance, "entreprise", None) and str(instance.entreprise)
        return data


class RecommandationSerializer(serializers.ModelSerializer):
    offre_detail = OffreRecommandeeSerializer(source="offre", read_only=True)

    class Meta:
        model = Recommandation
        fields = [
            "id", "offre", "offre_detail", "score_matching", "raison",
            "statut", "date_recommandation", "date_consultation",
        ]
        read_only_fields = fields


class RecommandationIgnorerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommandation
        fields = ["statut"]
        read_only_fields = ["statut"]