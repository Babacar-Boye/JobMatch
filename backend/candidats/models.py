from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from django.urls import reverse


# Create your models here.


class CV(models.Model):

    class StatutTraitement(models.TextChoices):
        EN_ATTENTE = "en_attente", _("En attente")
        EN_COURS = "en_cours", _("En cours d'analyse")
        TERMINE = "termine", _("Analyse terminée")
        ECHEC = "echec", _("Échec de l'analyse")

    chemin_fichier = models.FileField(upload_to="cv/", blank=True, null=True)
    nom_fichier_original = models.CharField(max_length=50)
    taille_fichier = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text=_("Taille du fichier en octets"),
    )
    texte_extrait = models.TextField(blank=True, null=True)
    langue = models.CharField(max_length=50, blank=True, null=True)

    # Champs ajoutés
    statut_traitement = models.CharField(
        max_length=20,
        choices=StatutTraitement.choices,
        default=StatutTraitement.EN_ATTENTE,
    )
    date_upload = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    candidat = models.OneToOneField(
        "account.Candidat",
        verbose_name=_("candidat"),
        on_delete=models.CASCADE,
        related_name="cv",
    )

    class Meta:
        verbose_name = _("CV")
        verbose_name_plural = _("CVs")
        db_table = "cv"
        ordering = ["-date_upload"]

    def __str__(self):
        return f"{self.nom_fichier_original} - {self.candidat}"


class Experience(models.Model):

    class TypeContrat(models.TextChoices):
        CDI = "cdi", _("CDI")
        CDD = "cdd", _("CDD")
        STAGE = "stage", _("Stage")
        FREELANCE = "freelance", _("Freelance")
        ALTERNANCE = "alternance", _("Alternance")
        BENEVOLAT = "benevolat", _("Bénévolat")

    poste = models.CharField(max_length=50)
    nom_entreprise = models.CharField(max_length=50)
    secteur = models.CharField(max_length=50, blank=True, null=True)
    localisation = models.CharField(max_length=50, blank=True, null=True)
    type_contrat = models.CharField(
        max_length=20, choices=TypeContrat.choices, blank=True, null=True
    )

    # Champs ajoutés
    description = models.TextField(
        blank=True, null=True, help_text=_("Description des missions et responsabilités")
    )
    competences_utilisees = models.ManyToManyField(
        "candidat.Competence", blank=True, related_name="experiences"
    )
    niveau_seniorite = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text=_("Ex: Junior, Confirmé, Senior, Manager"),
    )

    en_cours = models.BooleanField(default=False)
    date_debut = models.DateField()
    date_fin = models.DateField(
        blank=True,
        null=True,
        help_text=_("Laisser vide si l'expérience est en cours"),
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    cv = models.ForeignKey(
        "candidat.CV",
        verbose_name=_("cv"),
        on_delete=models.CASCADE,
        related_name="experiences",
    )

    class Meta:
        verbose_name = _("Expérience")
        verbose_name_plural = _("Expériences")
        db_table = "experience"
        ordering = ["-date_debut"]

    def __str__(self):
        return f"{self.poste} chez {self.nom_entreprise}"


class Competence(models.Model):

    class Categorie(models.TextChoices):
        TECHNIQUE = "technique", _("Compétence technique")
        LANGUE = "langue", _("Langue")
        SOFT_SKILL = "soft_skill", _("Savoir-être")
        OUTIL = "outil", _("Outil / Logiciel")
        CERTIFICATION = "certification", _("Certification")

    class Niveau(models.TextChoices):
        DEBUTANT = "debutant", _("Débutant")
        INTERMEDIAIRE = "intermediaire", _("Intermédiaire")
        AVANCE = "avance", _("Avancé")
        EXPERT = "expert", _("Expert")

    nom = models.CharField(max_length=50)
    categorie = models.CharField(
        max_length=20, choices=Categorie.choices, default=Categorie.TECHNIQUE
    )
    niveau = models.CharField(
        max_length=20, choices=Niveau.choices, blank=True, null=True
    )
    annees_experience = models.PositiveSmallIntegerField(blank=True, null=True)
    # extrait_par_ia = models.BooleanField(
    #     default=False,
    #     help_text=_("True si la compétence a été détectée automatiquement par l'IA"),
    # )

    cv = models.ForeignKey(
        "candidat.CV",
        verbose_name=_("cv"),
        on_delete=models.CASCADE,
        related_name="competences",
    )

    class Meta:
        verbose_name = _("Compétence")
        verbose_name_plural = _("Compétences")
        db_table = "competence"
        ordering = ["categorie", "nom"]

    def __str__(self):
        return self.nom


class Formation(models.Model):

    class NiveauDiplome(models.TextChoices):
        BAC = "bac", _("Baccalauréat")
        BAC_PLUS_2 = "bac_2", _("Bac+2 (BTS/DUT)")
        LICENCE = "licence", _("Licence / Bac+3")
        MASTER = "master", _("Master / Bac+5")
        DOCTORAT = "doctorat", _("Doctorat")
        AUTRE = "autre", _("Autre")

    intitule = models.CharField(max_length=100, help_text=_("Intitulé du diplôme"))
    etablissement = models.CharField(max_length=100)
    domaine_etude = models.CharField(max_length=100, blank=True, null=True)
    niveau_diplome = models.CharField(
        max_length=20, choices=NiveauDiplome.choices, blank=True, null=True
    )
    ville = models.CharField(max_length=50, blank=True, null=True)
    pays = models.CharField(max_length=50, blank=True, null=True)
    mention = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    en_cours = models.BooleanField(default=False)
    date_debut = models.DateField()
    date_fin = models.DateField(
        blank=True,
        null=True,
        help_text=_("Laisser vide si la formation est en cours"),
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    cv = models.ForeignKey(
        "candidat.CV",
        verbose_name=_("cv"),
        on_delete=models.CASCADE,
        related_name="formations",
    )

    class Meta:
        verbose_name = _("Formation")
        verbose_name_plural = _("Formations")
        db_table = "formation"
        ordering = ["-date_debut"]

    def __str__(self):
        return f"{self.intitule} - {self.etablissement}"
    
    








class Preference(models.Model):

    class TypeContratPrefere(models.TextChoices):
        CDI = "cdi", _("CDI")
        CDD = "cdd", _("CDD")
        STAGE = "stage", _("Stage")
        FREELANCE = "freelance", _("Freelance")
        ALTERNANCE = "alternance", _("Alternance")
        INDIFFERENT = "indifferent", _("Indifférent")

    class NiveauPosteSouhaite(models.TextChoices):
        STAGIAIRE = "stagiaire", _("Stagiaire")
        JUNIOR = "junior", _("Junior")
        CONFIRME = "confirme", _("Confirmé")
        SENIOR = "senior", _("Senior")
        MANAGER = "manager", _("Manager / Chef d'équipe")
        DIRECTION = "direction", _("Direction")

    class NiveauExperienceRecherchee(models.TextChoices):
        DEBUTANT = "debutant", _("Débutant (0-2 ans)")
        JUNIOR = "junior", _("Junior (2-5 ans)")
        CONFIRME = "confirme", _("Confirmé (5-10 ans)")
        SENIOR = "senior", _("Senior (10+ ans)")

    class ModeTravail(models.TextChoices):
        PRESENTIEL = "presentiel", _("Présentiel")
        TELETRAVAIL = "teletravail", _("Télétravail")
        HYBRIDE = "hybride", _("Hybride")
        INDIFFERENT = "indifferent", _("Indifférent")

    class FrequenceAlerte(models.TextChoices):
        IMMEDIATE = "immediate", _("Immédiate")
        QUOTIDIENNE = "quotidienne", _("Quotidienne")
        HEBDOMADAIRE = "hebdomadaire", _("Hebdomadaire")

    # Relation : un candidat a un seul jeu de préférences
    candidat = models.OneToOneField(
        "account.Candidat",
        verbose_name=_("candidat"),
        on_delete=models.CASCADE,
        related_name="preference",
    )

    # Attributs du diagramme
    secteurs_preferes = models.JSONField(
        default=list,
        blank=True,
        help_text=_("Liste des secteurs d'activité recherchés (ex: technologie, finance...)"),
    )
    type_contrat_prefere = models.CharField(
        max_length=20,
        choices=TypeContratPrefere.choices,
        default=TypeContratPrefere.INDIFFERENT,
    )
    salaire_min_souhaite = models.PositiveIntegerField(
        blank=True, null=True, validators=[MinValueValidator(0)]
    )
    niveau_poste_souhaite = models.CharField(
        max_length=20, choices=NiveauPosteSouhaite.choices, blank=True, null=True
    )
    date_maj = models.DateField(auto_now=True)
    mode_travail = models.CharField(
        max_length=20, choices=ModeTravail.choices, default=ModeTravail.INDIFFERENT
    )
    niveau_experience_recherchee = models.CharField(
        max_length=20, choices=NiveauExperienceRecherchee.choices, blank=True, null=True
    )

    # Champs ajoutés
    # devise = models.CharField(max_length=10, default="FCFA")
    villes_preferees = models.JSONField(
        default=list,
        blank=True,
        help_text=_("Villes où le candidat souhaite travailler"),
    )
    
    mots_cles = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Mots-clés libres utilisés pour affiner les suggestions d'offres"),
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        verbose_name = _("Préférence")
        verbose_name_plural = _("Préférences")
        db_table = "preference"

    def __str__(self):
        return f"Préférences de {self.candidat}"

    def get_absolute_url(self):
        return reverse("preference_detail", kwargs={"pk": self.pk})

    # Méthodes du diagramme
    def mettre_a_jour(self, **kwargs):
        """Met à jour un ou plusieurs champs de préférence en une seule fois."""
        champs_autorises = {f.name for f in self._meta.get_fields()}
        for champ, valeur in kwargs.items():
            if champ in champs_autorises:
                setattr(self, champ, valeur)
        self.save()

    def activer_alerte(self, actif=True):
        self.alerte_active = actif
        self.save()