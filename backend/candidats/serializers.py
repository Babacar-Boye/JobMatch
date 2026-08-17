from rest_framework import serializers
from .models import CV, Experience, Competence, Formation, Preference


class CVSerializer(serializers.ModelSerializer):

    class Meta:
        model = CV
        fields = [
            "id",
            "chemin_fichier",
            "nom_fichier_original",
            "taille_fichier",
            "texte_extrait",
            "langue",
            "statut_traitement",
            "date_upload",
            "date_modification",
            "candidat",
        ]

        read_only_fields = [
            "id",
            "taille_fichier",
            "texte_extrait",
            "langue",
            "statut_traitement",
            "date_upload",
            "date_modification",
        ]
        
    def create(self, validated_data):
        fichier = validated_data.get("chemin_fichier")

        if fichier:
            validated_data["nom_fichier_original"] = fichier.name
            validated_data["taille_fichier"] = fichier.size

        return CV.objects.create(**validated_data)









class ExperienceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Experience
        fields = [
            "id",
            "poste",
            "nom_entreprise",
            "secteur",
            "localisation",
            "type_contrat",
            "description",
            "niveau_seniorite",
            "en_cours",
            "date_debut",
            "date_fin",
            "date_creation",
            "cv",
        ]

        read_only_fields = [
            "id",
            "date_creation",
        ]


class CompetenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Competence
        fields = [
            "id",
            "nom",
            "categorie",
            "niveau",
            "annees_experience",
            "cv",
        ]

        read_only_fields = [
            "id",
        ]


class FormationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Formation
        fields = [
            "id",
            "intitule",
            "etablissement",
            "domaine_etude",
            "niveau_diplome",
            "ville",
            "pays",
            "mention",
            "description",
            "en_cours",
            "date_debut",
            "date_fin",
            "date_creation",
            "cv",
        ]

        read_only_fields = [
            "id",
            "date_creation",
        ]


class PreferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Preference
        fields = [
            "id",
            "candidat",
            "secteurs_preferes",
            "type_contrat_prefere",
            "salaire_min_souhaite",
            "niveau_poste_souhaite",
            "date_maj",
            "mode_travail",
            "niveau_experience_recherchee",
            "villes_preferees",
            "mots_cles",
            "date_creation",
        ]

        read_only_fields = [
            "id",
            "date_maj",
            "date_creation",
        ]