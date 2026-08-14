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

    class NiveauExperience(models.TextChoices):
        DEBUTANT = "debutant", _("Débutant (0-2 ans)")
        JUNIOR = "junior", _("Junior (2-5 ans)")
        CONFIRME = "confirme", _("Confirmé (5-10 ans)")
        SENIOR = "senior", _("Senior (10+ ans)")

    class NiveauEtudes(models.TextChoices):
        BAC = "bac", _("Baccalauréat")
        BAC_PLUS_2 = "bac_2", _("Bac+2 (BTS/DUT)")
        LICENCE = "licence", _("Licence / Bac+3")
        MASTER = "master", _("Master / Bac+5")
        DOCTORAT = "doctorat", _("Doctorat")
        INDIFFERENT = "indifferent", _("Indifférent")

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
    competences_requises = models.ManyToManyField(
        "candidat.Competence",
        through="CompetenceRequise",
        related_name="offres",
        blank=True,
    )

    # Contenu
    titre = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
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
        default=NiveauEtudes.INDIFFERENT,
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

    # Matching IA
    embedding_genere = models.BooleanField(
        default=False,
        help_text=_("Indique si l'embedding sémantique de l'offre a été calculé (mistral-embed)"),
    )
    mots_cles_ia = models.TextField(
        blank=True,
        null=True,
        help_text=_("Mots-clés extraits automatiquement pour le matching"),
    )

    # Statut / cycle de vie
    statut = models.CharField(
        max_length=20, choices=Statut.choices, default=Statut.BROUILLON
    )
    nombre_vues = models.PositiveIntegerField(default=0)

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

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.titre}-{self.entreprise.raison_sociale}")
            self.slug = base_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("offre_detail", kwargs={"slug": self.slug})

    @property
    def est_expiree(self):
        return bool(self.date_expiration and self.date_expiration < timezone.now().date())

    @property
    def nombre_candidatures(self):
        return self.candidatures.count() if hasattr(self, "candidatures") else 0


class CompetenceRequise(models.Model):
    """Table intermédiaire entre OffreEmploi et Competence, pondérée pour le matching IA."""

    class NiveauRequis(models.TextChoices):
        DEBUTANT = "debutant", _("Débutant")
        INTERMEDIAIRE = "intermediaire", _("Intermédiaire")
        AVANCE = "avance", _("Avancé")
        EXPERT = "expert", _("Expert")

    offre = models.ForeignKey(
        "offre.OffreEmploi", on_delete=models.CASCADE, related_name="exigences_competences"
    )
    
    competence = models.ForeignKey(
        "candidat.Competence", on_delete=models.CASCADE, related_name="exigences_offres"
    )
    
    niveau_requis = models.CharField(
        max_length=20, choices=NiveauRequis.choices, blank=True, null=True
    )
    obligatoire = models.BooleanField(
        default=True, help_text=_("Compétence indispensable ou simplement un plus")
    )
    poids = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text=_("Poids de la compétence dans le calcul du score de matching"),
    )

    class Meta:
        verbose_name = _("Compétence requise")
        verbose_name_plural = _("Compétences requises")
        db_table = "competence_requise"
        unique_together = ("offre", "competence")

    def __str__(self):
        return f"{self.competence} pour {self.offre}"