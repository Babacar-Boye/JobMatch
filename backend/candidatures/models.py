from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Candidature(models.Model):

    class Statut(models.TextChoices):
        ENVOYEE = "envoyee", _("Envoyée")
        VUE = "vue", _("Vue par le recruteur")
        PRESELECTIONNEE = "preselectionnee", _("Présélectionnée")
        ENTRETIEN = "entretien", _("Entretien programmé")
        ACCEPTEE = "acceptee", _("Acceptée")
        REFUSEE = "refusee", _("Refusée")
        RETIREE = "retiree", _("Retirée par le candidat")

    # Relations principales
    candidat = models.ForeignKey(
        "account.Candidat",
        verbose_name=_("candidat"),
        on_delete=models.CASCADE,
        related_name="candidatures",
    )
    offre = models.ForeignKey(
        "offre.OffreEmploi",
        verbose_name=_("offre d'emploi"),
        on_delete=models.CASCADE,
        related_name="candidatures",
    )

    # Contenu de la candidature
    lettre_motivation = models.FileField(upload_to = "candidature/lettre_motivation/" ,blank=True, null=True)
    message_candidat = models.TextField(
        blank=True, null=True, help_text=_("Message libre accompagnant la candidature")
    )

    # Matching / IA
    score_matching = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text=_("Score de compatibilité candidat/offre calculé par l'IA (0 à 100)"),
    )
    analyse_ia = models.TextField(
        blank=True,
        null=True,
        help_text=_("Synthèse générée par l'IA sur l'adéquation candidat/offre"),
    )
    points_forts = models.TextField(
        blank=True, null=True, help_text=_("Points forts identifiés par l'IA")
    )
    points_faibles = models.TextField(
        blank=True, null=True, help_text=_("Écarts identifiés par l'IA par rapport à l'offre")
    )

    # Suivi / statut
    statut = models.CharField(
        max_length=20, choices=Statut.choices, default=Statut.ENVOYEE
    )
    note_recruteur = models.TextField(
        blank=True, null=True, help_text=_("Notes internes du recruteur, non visibles du candidat")
    )
    est_favorite = models.BooleanField(
        default=False, help_text=_("Marquée comme favorite par le recruteur")
    )
    
    score_competences = models.FloatField(null=True, blank=True)
    score_experience = models.FloatField(null=True, blank=True)
    score_formation = models.FloatField(null=True, blank=True)
    
    score_global = models.FloatField(null=True, blank=True)

    # Dates
    date_candidature = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    

    class Meta:
        verbose_name = _("Candidature")
        verbose_name_plural = _("Candidatures")
        db_table = "candidature"
        ordering = ["-date_candidature"]
        # Un candidat ne peut postuler qu'une seule fois à la même offre
        unique_together = ("candidat", "offre")

    def __str__(self):
        return f"{self.candidat} → {self.offre} ({self.get_statut_display()})"

    def get_absolute_url(self):
        return reverse("candidature_detail", kwargs={"pk": self.pk})


class PieceJointe(models.Model):

    class TypePiece(models.TextChoices):
        PORTFOLIO = "portfolio", _("Portfolio")
        DIPLOME = "diplome", _("Diplôme / Certificat")
        RECOMMANDATION = "recommandation", _("Lettre de recommandation")
        AUTRE = "autre", _("Autre")

    candidature = models.ForeignKey(
        "candidature.Candidature",
        verbose_name=_("candidature"),
        on_delete=models.CASCADE,
        related_name="pieces_jointes",
    )

    # Champs ajoutés
    fichier = models.FileField(upload_to="pieces_jointes/")
    nom_fichier_original = models.CharField(max_length=100)
    type_piece = models.CharField(
        max_length=30, choices=TypePiece.choices, default=TypePiece.AUTRE
    )
    taille_fichier = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text=_("Taille du fichier en octets"),
    )
    description = models.CharField(max_length=255, blank=True, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Pièce jointe")
        verbose_name_plural = _("Pièces jointes")
        db_table = "piece_jointe"
        ordering = ["-date_ajout"]

    def __str__(self):
        return f"{self.nom_fichier_original} ({self.get_type_piece_display()})"

    def get_absolute_url(self):
        return reverse("piece_jointe_detail", kwargs={"pk": self.pk})