from rest_framwork import serializers
from .models import OffreEmploi, CompetenceRequise


class CompetenceRequiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetenceRequise
        fields = ["id", "nom", "description"]



class OffreEmploiListSerializer(serializers.ModelSerializer):
    """
    Serializer allégé pour l'affichage en liste (résultats de recherche,
    listing paginé). On évite les champs volumineux (description, missions...).
    """

    entreprise_nom = serializers.CharField(source="entreprise.nom", read_only=True)
    type_contrat_display = serializers.CharField(
        source="get_type_contrat_display", read_only=True
    )
    mode_travail_display = serializers.CharField(
        source="get_mode_travail_display", read_only=True
    )
    est_expiree = serializers.BooleanField(read_only=True)

    class Meta:
        model = OffreEmploi
        fields = [
            "id",
            "slug",
            "titre",
            "entreprise_nom",
            "ville",
            "pays",
            "type_contrat",
            "type_contrat_display",
            "mode_travail",
            "mode_travail_display",
            "salaire_min",
            "salaire_max",
            "devise",
            "salaire_visible",
            "est_urgente",
            "statut",
            "date_publication",
            "est_expiree",
        ]


class OffreEmploiDetailSerializer(serializers.ModelSerializer):
    """
    Serializer complet pour la page de détail d'une offre (lecture publique
    ou vue recruteur). Inclut les compétences requises et les infos calculées.
    """

    entreprise_nom = serializers.CharField(source="entreprise.nom", read_only=True)
    entreprise_logo = serializers.ImageField(
        source="entreprise.logo", read_only=True, allow_null=True
    )
    competences_requises = CompetenceRequiseSerializer(many=True, read_only=True)

    type_contrat_display = serializers.CharField(
        source="get_type_contrat_display", read_only=True
    )
    niveau_experience_display = serializers.CharField(
        source="get_niveau_experience_display", read_only=True
    )
    niveau_etudes_display = serializers.CharField(
        source="get_niveau_etudes_display", read_only=True
    )
    mode_travail_display = serializers.CharField(
        source="get_mode_travail_display", read_only=True
    )
    statut_display = serializers.CharField(source="get_statut_display", read_only=True)

    est_expiree = serializers.BooleanField(read_only=True)
    nombre_candidatures = serializers.IntegerField(read_only=True)

    class Meta:
        model = OffreEmploi
        fields = [
            "id",
            "slug",
            "titre",
            "description",
            "missions",
            "profil_recherche",
            "avantages",
            "entreprise_nom",
            "entreprise_logo",
            "type_contrat",
            "type_contrat_display",
            "niveau_experience",
            "niveau_experience_display",
            "niveau_etudes",
            "niveau_etudes_display",
            "mode_travail",
            "mode_travail_display",
            "ville",
            "pays",
            "salaire_min",
            "salaire_max",
            "devise",
            "salaire_visible",
            "nombre_postes",
            "est_urgente",
            "statut",
            "statut_display",
            "date_publication",
            "date_expiration",
            "date_creation",
            "date_modification",
            "competences_requises",
            "est_expiree",
            "nombre_candidatures",
        ]


class OffreEmploiCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer pour la création/édition par le recruteur.
    Gère l'écriture imbriquée des compétences requises et quelques validations.
    """

    competences_requises = CompetenceRequiseSerializer(many=True, required=False)

    class Meta:
        model = OffreEmploi
        fields = [
            "id",
            "titre",
            "description",
            "missions",
            "profil_recherche",
            "avantages",
            "type_contrat",
            "niveau_experience",
            "niveau_etudes",
            "mode_travail",
            "ville",
            "pays",
            "salaire_min",
            "salaire_max",
            "devise",
            "salaire_visible",
            "nombre_postes",
            "est_urgente",
            "poids_competence",
            "poids_experience",
            "poids_formation",
            "statut",
            "date_publication",
            "date_expiration",
            "competences_requises",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        salaire_min = attrs.get("salaire_min", getattr(self.instance, "salaire_min", None))
        salaire_max = attrs.get("salaire_max", getattr(self.instance, "salaire_max", None))
        if salaire_min and salaire_max and salaire_min > salaire_max:
            raise serializers.ValidationError(
                {"salaire_min": "Le salaire minimum ne peut pas dépasser le salaire maximum."}
            )

        poids = [
            data.get("poids_competence"),
            data.get("poids_experience"),
            data.get("poids_formation"),
        ]
        if all(p is not None for p in poids):
            if sum(poids) != 100:
                raise serializers.ValidationError(
                    "La somme des poids (compétence + expérience + formation) doit être égale à 100."
                )
                
        return attrs

    def create(self, validated_data):
        competences_data = validated_data.pop("competences_requises", [])
        # entreprise et recruteur à injecter depuis la vue (ex: request.user)
        offre = OffreEmploi.objects.create(**validated_data)
        for competence in competences_data:
            CompetenceRequise.objects.create(offre=offre, **competence)
        return offre

    def update(self, instance, validated_data):
        competences_data = validated_data.pop("competences_requises", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if competences_data is not None:
            instance.competences_requises.all().delete()
            for competence in competences_data:
                CompetenceRequise.objects.create(offre=instance, **competence)

        return instance