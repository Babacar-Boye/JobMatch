from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import URLValidator, RegexValidator

# Create your models here.


class Entreprise(models.Model):

    class SecteurActivite(models.TextChoices):
        TECHNOLOGIE = "technologie", _("Technologie / Informatique")
        FINANCE = "finance", _("Finance / Banque / Assurance")
        SANTE = "sante", _("Santé")
        EDUCATION = "education", _("Éducation / Formation")
        COMMERCE = "commerce", _("Commerce / Distribution")
        INDUSTRIE = "industrie", _("Industrie / BTP")
        AGRICULTURE = "agriculture", _("Agriculture / Agroalimentaire")
        TELECOM = "telecom", _("Télécommunications")
        TOURISME = "tourisme", _("Tourisme / Hôtellerie")
        TRANSPORT = "transport", _("Transport / Logistique")
        ADMINISTRATION = "administration", _("Administration publique")
        ONG = "ong", _("ONG / Associatif")
        AUTRE = "autre", _("Autre")

    class TailleEffectif(models.TextChoices):
        TPE = "tpe", _("1 à 9 salariés")
        PE = "pe", _("10 à 49 salariés")
        PME = "pme", _("50 à 249 salariés")
        ETI = "eti", _("250 à 999 salariés")
        GE = "ge", _("1000 salariés et plus")

    class StatutVerification(models.TextChoices):
        EN_ATTENTE = "en_attente", _("En attente de vérification")
        VERIFIEE = "verifiee", _("Vérifiée")
        REJETEE = "rejetee", _("Rejetée")

    # Identité de l'entreprise
    raison_sociale = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    logo = models.ImageField(upload_to="entreprises/logos/", blank=True, null=True)
    banniere = models.ImageField(upload_to="entreprises/bannieres/", blank=True, null=True)
    description = models.TextField(
        blank=True, null=True, help_text=_("Présentation générale de l'entreprise")
    )

    # Classification
    secteur_activite = models.CharField(
        max_length=30, choices=SecteurActivite.choices, default=SecteurActivite.AUTRE
    )
    taille_effectif = models.CharField(
        max_length=10, choices=TailleEffectif.choices, blank=True, null=True
    )
    date_creation_entreprise = models.DateField(
        blank=True, null=True, help_text=_("Date de création/fondation de l'entreprise")
    )

    # Identifiants légaux (contexte Sénégal)
    ninea = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        unique=True,
        verbose_name="NINEA",
        help_text=_("Numéro d'Identification Nationale des Entreprises et Associations"),
    )
    registre_commerce = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name=_("Registre de commerce (RCCM)"),
    )

    # Coordonnées
    email_contact = models.EmailField(blank=True, null=True)
    telephone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r"^\+?[0-9\s]{7,20}$",
                message=_("Numéro de téléphone invalide"),
            )
        ],
    )
    site_web = models.URLField(blank=True, null=True, validators=[URLValidator()])
    linkedin_url = models.URLField(blank=True, null=True)

    # Localisation
    adresse = models.CharField(max_length=255, blank=True, null=True)
    ville = models.CharField(max_length=50, blank=True, null=True)
    pays = models.CharField(max_length=50, default="Sénégal")

    # Modération / confiance
    statut_verification = models.CharField(
        max_length=20,
        choices=StatutVerification.choices,
        default=StatutVerification.EN_ATTENTE,
    )
    date_verification = models.DateTimeField(blank=True, null=True)
    est_active = models.BooleanField(
        default=True, help_text=_("Permet de désactiver un compte entreprise sans le supprimer")
    )

    # Suivi
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Entreprise")
        verbose_name_plural = _("Entreprises")
        db_table = "entreprise"
        ordering = ["raison_sociale"]

    def __str__(self):
        return self.raison_sociale

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.raison_sociale)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("entreprise_detail", kwargs={"slug": self.slug})

    @property
    def nombre_offres_actives(self):
        """Nombre d'offres d'emploi actuellement publiées par l'entreprise."""
        return self.offres.filter(est_active=True).count() if hasattr(self, "offres") else 0