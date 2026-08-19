from rest_framework import serializers
from .models import Candidature, PieceJointe


class PieceJointeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PieceJointe
        fields = [
            "id", "candidature", "fichier", "nom_fichier_original",
            "type_piece", "taille_fichier", "description", "date_ajout",
        ]
        read_only_fields = ["id", "candidature", "nom_fichier_original", "taille_fichier", "date_ajout"]


class CandidatureCreateSerializer(serializers.ModelSerializer):
    diplome = serializers.FileField(write_only=True, required=False)
    lettre_recommandation = serializers.FileField(write_only=True, required=False)
    portfolio = serializers.FileField(write_only=True, required=False)
    autres = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )
    pieces_jointes = PieceJointeSerializer(many=True, read_only=True)

    class Meta:
        model = Candidature
        fields = [
            "id", "offre", "message_candidat", "lettre_motivation",
            "diplome", "lettre_recommandation", "portfolio", "autres",
            "pieces_jointes",
        ]

    def validate(self, data):
        max_size = 5 * 1024 * 1024
        extensions_autorisees = [".pdf", ".doc", ".docx", ".jpg", ".png"]

        offre = data.get("offre")
        pieces_requises = getattr(offre, "pieces_requises", []) if offre else []

        if "diplome" in pieces_requises and not data.get("diplome"):
            raise serializers.ValidationError({"diplome": "Cette pièce est requise pour cette offre."})
        if "lettre_recommandation" in pieces_requises and not data.get("lettre_recommandation"):
            raise serializers.ValidationError({"lettre_recommandation": "Cette pièce est requise pour cette offre."})
        if "portfolio" in pieces_requises and not data.get("portfolio"):
            raise serializers.ValidationError({"portfolio": "Cette pièce est requise pour cette offre."})

        fichiers = [
            data.get("lettre_motivation"),
            data.get("diplome"),
            data.get("lettre_recommandation"),
            data.get("portfolio"),
            *data.get("autres", []),
        ]
        for f in fichiers:
            if not f:
                continue
            if f.size > max_size:
                raise serializers.ValidationError(f"{f.name} dépasse 5 Mo.")
            if not any(f.name.lower().endswith(ext) for ext in extensions_autorisees):
                raise serializers.ValidationError(f"{f.name} : format non autorisé.")

        return data

    def create(self, validated_data):
        diplome = validated_data.pop("diplome", None)
        lettre_recommandation = validated_data.pop("lettre_recommandation", None)
        portfolio = validated_data.pop("portfolio", None)
        autres = validated_data.pop("autres", [])

        candidature = Candidature.objects.create(
            candidat=self.context["request"].user.candidat,
            **validated_data,
        )

        if diplome:
            PieceJointe.objects.create(
                candidature=candidature, fichier=diplome,
                nom_fichier_original=diplome.name, taille_fichier=diplome.size,
                type_piece=PieceJointe.TypePiece.DIPLOME,
            )
        if lettre_recommandation:
            PieceJointe.objects.create(
                candidature=candidature, fichier=lettre_recommandation,
                nom_fichier_original=lettre_recommandation.name, taille_fichier=lettre_recommandation.size,
                type_piece=PieceJointe.TypePiece.RECOMMANDATION,
            )
        if portfolio:
            PieceJointe.objects.create(
                candidature=candidature, fichier=portfolio,
                nom_fichier_original=portfolio.name, taille_fichier=portfolio.size,
                type_piece=PieceJointe.TypePiece.PORTFOLIO,
            )
        for f in autres:
            PieceJointe.objects.create(
                candidature=candidature, fichier=f,
                nom_fichier_original=f.name, taille_fichier=f.size,
                type_piece=PieceJointe.TypePiece.AUTRE,
            )

        return candidature


class CandidatureCandidatSerializer(serializers.ModelSerializer):
    pieces_jointes = PieceJointeSerializer(many=True, read_only=True)

    class Meta:
        model = Candidature
        fields = [
            "id", "offre", "message_candidat", "lettre_motivation",
            "statut", "score_matching", "analyse_ia", "points_forts",
            "points_faibles", "pieces_jointes", "date_candidature", "date_modification",
        ]
        read_only_fields = fields


class CandidatureRecruteurSerializer(serializers.ModelSerializer):
    pieces_jointes = PieceJointeSerializer(many=True, read_only=True)

    class Meta:
        model = Candidature
        fields = "__all__"
        read_only_fields = [
            "candidat", "offre", "message_candidat", "lettre_motivation",
            "score_matching", "score_competences", "score_experience",
            "score_formation", "score_global", "analyse_ia",
            "points_forts", "points_faibles", "date_candidature", "date_modification",
        ]