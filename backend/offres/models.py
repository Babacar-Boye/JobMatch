from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class OffreEmploi(models.Model):

    class TypeContrat(models.TextChoices):
        CDI = "cdi", _("CDI")
        CDD = "cdd", _("CDD")
        STAGE = "stage", _("Stage")
        FREELANCE = "freelance", _("Freelance")
        ALTERNANCE = "alternance", _("Alternance")
        INTERIM = "interim", _("Intérim")
        
    class NiveauEtudes(models.TextChoices):
        AUCUN = "aucun", _("Aucun diplôme requis")
        BAC = "bac", _("Baccalauréat")
        BAC2 = "bac2", _("Bac +2")
        BAC3 = "bac3", _("Bac +3 / Licence")
        BAC4 = "bac4", _("Bac +4")
        BAC5 = "bac5", _("Bac +5 / Master")
        DOCTORAT = "doctorat", _("Doctorat")

    class NiveauExperience(models.TextChoices):
        DEBUTANT = "debutant", _("Débutant")
        JUNIOR = "junior", _("1 à 2 ans")
        INTERMEDIAIRE = "intermediaire", _("3 à 5 ans")
        SENIOR = "senior", _("5 à 10 ans")
        EXPERT = "expert", _("Plus de 10 ans")
        
    class ModeTravail(models.TextChoices):
        PRESENTIEL = "presentiel", _("Présentiel")
        TELETRAVAIL = "teletravail", _("Télétravail")
        HYBRIDE = "hybride", _("Hybride")

    class Statut(models.TextChoices):
        BROUILLON = "brouillon", _("Brouillon")
        EN_ATTENTE = "en_attente", _("En attente de validation")
        PUBLIEE = "publiee", _("Publiée")
        EXPIREE = "expiree", _("Expirée")
        POURVUE = "pourvue", _("Pourvue")
        ARCHIVEE = "archivee", _("Archivée")

    # Relations
    entreprise = models.ForeignKey(
        "entreprise.Entreprise",
        verbose_name=_("entreprise"),
        on_delete=models.CASCADE,
        related_name="offres",
    )
    recruteur = models.ForeignKey(
        "account.Recruteur",
        verbose_name=_("recruteur"),
        on_delete=models.CASCADE,
        related_name="offres_publiees",
        help_text=_("Recruteur ayant publié l'offre"),
    )

    # Contenu
    titre = models.CharField(max_length=150)
    description = models.TextField(help_text=_("Description générale du poste"))
    missions = models.TextField(blank=True, null=True)
    profil_recherche = models.TextField(
        blank=True, null=True, help_text=_("Profil, qualités et prérequis attendus")
    )
    avantages = models.TextField(blank=True, null=True)

    # Classification
    type_contrat = models.CharField(max_length=20, choices=TypeContrat.choices)
    niveau_experience = models.CharField(
        max_length=20, choices=NiveauExperience.choices, blank=True, null=True
    )
    niveau_etudes = models.CharField(
        max_length=20,
        choices=NiveauEtudes.choices,
        blank=True,
        null=True
    )
    mode_travail = models.CharField(
        max_length=20, choices=ModeTravail.choices, default=ModeTravail.PRESENTIEL
    )

    # Localisation
    ville = models.CharField(max_length=50, blank=True, null=True)
    pays = models.CharField(max_length=50, default="Sénégal")

    # Rémunération
    salaire_min = models.PositiveIntegerField(blank=True, null=True)
    salaire_max = models.PositiveIntegerField(blank=True, null=True)
    devise = models.CharField(max_length=10, default="FCFA")
    salaire_visible = models.BooleanField(
        default=False, help_text=_("Afficher la fourchette salariale sur l'offre publique")
    )

    # Volume / urgence
    nombre_postes = models.PositiveSmallIntegerField(default=1)
    est_urgente = models.BooleanField(default=False)
    
    poids_competence = models.PositiveIntegerField(blank=True, null=True)
    poids_experience = models.PositiveIntegerField(blank=True, null=True)
    poids_formation = models.PositiveIntegerField(blank=True, null=True)

    # Statut / cycle de vie
    statut = models.CharField(
        max_length=20, choices=Statut.choices, default=Statut.BROUILLON
    )

    # Dates
    date_publication = models.DateTimeField(blank=True, null=True)
    date_expiration = models.DateField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Offre d'emploi")
        verbose_name_plural = _("Offres d'emploi")
        db_table = "offre_emploi"
        ordering = ["-date_publication", "-date_creation"]

    def __str__(self):
        return f"{self.titre} - {self.entreprise}"

    def get_absolute_url(self):
        return reverse("offre_detail", kwargs={"slug": self.slug})

    @property
    def est_expiree(self):
        return bool(self.date_expiration and self.date_expiration < timezone.now().date())

    @property
    def nombre_candidatures(self):
        return self.candidatures.count() if hasattr(self, "candidatures") else 0


class Competence(models.Model):
    
    offre = models.ForeignKey("OffreEmploi", verbose_name=_("OffreEmploi"), on_delete=models.CASCADE)
    nom = models.CharField(
        max_length=100,
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    categorie = models.ForeignKey(
        CategorieCompetence,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="competences"
    )

    def __str__(self):
        return self.nom