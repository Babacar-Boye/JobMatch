from rest_framework import serializers
from .models import Entretien, Evaluation, CritereEvaluation


class CritereEvaluationSerializer(serializers.ModelSerializer):
    """
    Serializer pour un critère d'évaluation.
    Utilisé en nested (imbriqué) dans EvaluationSerializer.
    """

    class Meta:
        model = CritereEvaluation
        fields = [
            "id",
            "evaluation",
            "libelle",
            "categorie",
            "note",
            "noteMax",
            "commentaire",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            # evaluation devient optionnel/en lecture quand on écrit via le nested serializer
            "evaluation": {"required": False}
        }

    def validate(self, data):
        note = data.get("note", getattr(self.instance, "note", None))
        note_max = data.get("noteMax", getattr(self.instance, "noteMax", None))
        if note is not None and note_max is not None and note > note_max:
            raise serializers.ValidationError(
                "La note ne peut pas dépasser la note maximale (noteMax)."
            )
        return data


class EvaluationSerializer(serializers.ModelSerializer):
    """
    Serializer pour une évaluation, avec ses critères imbriqués (nested).
    Permet la création/mise à jour des critères en même temps que l'évaluation.
    """

    criteres = CritereEvaluationSerializer(many=True, required=False)

    class Meta:
        model = Evaluation
        fields = [
            "id",
            "entretien",
            "noteGlobale",
            "commentaireGlobale",
            "pointForts",
            "pointAmeliorer",
            "decision",
            "dateEvaluation",
            "criteres",
        ]
        read_only_fields = ["id", "noteGlobale"]

    def create(self, validated_data):
        criteres_data = validated_data.pop("criteres", [])
        evaluation = Evaluation.objects.create(**validated_data)
        for critere_data in criteres_data:
            CritereEvaluation.objects.create(evaluation=evaluation, **critere_data)
        evaluation.calculerNoteGlobale()
        return evaluation

    def update(self, instance, validated_data):
        criteres_data = validated_data.pop("criteres", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if criteres_data is not None:
            # on remplace les critères existants par la nouvelle liste
            instance.criteres.all().delete()
            for critere_data in criteres_data:
                CritereEvaluation.objects.create(evaluation=instance, **critere_data)

        instance.calculerNoteGlobale()
        return instance


class EntretienSerializer(serializers.ModelSerializer):
    """
    Serializer pour un entretien.
    Expose l'évaluation liée en lecture seule (si elle existe déjà).
    """

    evaluation = EvaluationSerializer(read_only=True)

    class Meta:
        model = Entretien
        fields = [
            "id",
            "format",
            "statut",
            "lienVisio",
            "adresseLieu",
            "rappelEnvoye",
            "noteRecruteur",
            "dateHeure",
            "dateCreation",
            "evaluation",
        ]
        read_only_fields = ["id", "dateCreation", "rappelEnvoye", "lienVisio"]


class EntretienCreateSerializer(serializers.ModelSerializer):
    """
    Serializer allégé pour la création d'un entretien
    (sans les champs générés automatiquement).
    """

    class Meta:
        model = Entretien
        fields = [
            "id",
            "format",
            "adresseLieu",
            "dateHeure",
        ]
        read_only_fields = ["id"]