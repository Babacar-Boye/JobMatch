from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Entretien(models.Model):

    class Format(models.TextChoices):
        PRESENTIEL = "presentiel", _("Présentiel")
        VISIOCONFERENCE = "visio", _("Visioconférence")
        TELEPHONIQUE = "telephonique", _("Téléphonique")

    class Statut(models.TextChoices):
        PLANIFIE = "planifie", _("Planifié")
        CONFIRME = "confirme", _("Confirmé")
        REPROGRAMME = "reprogramme", _("Reprogrammé")
        ANNULE = "annule", _("Annulé")
        TERMINE = "termine", _("Terminé")

    # Relations
    candidature = models.ForeignKey(
        "candidature.Candidature",
        verbose_name=_("candidature"),
        on_delete=models.CASCADE,
        related_name="entretiens",
    )
    recruteur = models.ForeignKey(
        "account.Recruteur",
        verbose_name=_("recruteur en charge"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="entretiens_menes",
    )

    # Attributs du diagramme
    format = models.CharField(max_length=20, choices=Format.choices, default=Format.VISIOCONFERENCE)
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.PLANIFIE)
    lien_visio = models.URLField(blank=True, null=True)
    adresse_lieu = models.CharField(max_length=255, blank=True, null=True)
    rappel_envoye = models.BooleanField(default=False)
    note_recruteur = models.TextField(
        blank=True, null=True, help_text=_("Notes internes prises par le recruteur")
    )
    date_heure = models.DateTimeField(help_text=_("Date et heure prévues de l'entretien"))
    date_creation = models.DateTimeField(auto_now_add=True)

    # Champs ajoutés
    duree_minutes = models.PositiveSmallIntegerField(
        default=30, help_text=_("Durée prévue de l'entretien en minutes")
    )
    motif_annulation = models.CharField(max_length=255, blank=True, null=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Entretien")
        verbose_name_plural = _("Entretiens")
        db_table = "entretien"
        ordering = ["-date_heure"]

    def __str__(self):
        return f"Entretien {self.get_format_display()} - {self.candidature} ({self.date_heure:%d/%m/%Y %H:%M})"

    def get_absolute_url(self):
        return reverse("entretien_detail", kwargs={"pk": self.pk})

    # Méthodes du diagramme (comportements métier de base)
    def planifier(self, date_heure, format=None):
        self.date_heure = date_heure
        if format:
            self.format = format
        self.statut = self.Statut.PLANIFIE
        self.save()

    def confirmer(self):
        self.statut = self.Statut.CONFIRME
        self.save()

    def annuler(self, motif=None):
        self.statut = self.Statut.ANNULE
        if motif:
            self.motif_annulation = motif
        self.save()

    def reprogrammer(self, nouvelle_date_heure):
        self.date_heure = nouvelle_date_heure
        self.statut = self.Statut.REPROGRAMME
        self.rappel_envoye = False
        self.save()

    def envoyer_rappel(self):
        self.rappel_envoye = True
        self.save()

    def terminer(self):
        self.statut = self.Statut.TERMINE
        self.save()

    def generer_lien_visio(self):
        """Génère (ou régénère) le lien de visioconférence de l'entretien."""
        # Intégration à brancher avec un service externe (Jitsi, Google Meet, etc.)
        self.lien_visio = f"https://meet.jobmatch-ai.sn/entretien-{self.pk}"
        self.save()
        return self.lien_visio


class Evaluation(models.Model):

    class Decision(models.TextChoices):
        FAVORABLE = "favorable", _("Avis favorable")
        DEFAVORABLE = "defavorable", _("Avis défavorable")
        A_REVOIR = "a_revoir", _("À revoir")
        LISTE_ATTENTE = "liste_attente", _("Liste d'attente")

    # Relation "faire_objet" (1 - 1)
    entretien = models.OneToOneField(
        "entretien.Entretien",
        verbose_name=_("entretien évalué"),
        on_delete=models.CASCADE,
        related_name="evaluation",
    )
    evaluateur = models.ForeignKey(
        "account.Recruteur",
        verbose_name=_("évaluateur"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="evaluations_realisees",
    )

    # Attributs du diagramme
    note_globale = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        help_text=_("Note globale sur 20, calculée à partir des critères"),
    )
    commentaire_globale = models.TextField(blank=True, null=True)
    point_forts = models.TextField(blank=True, null=True)
    point_ameliorer = models.TextField(blank=True, null=True)
    decision = models.CharField(
        max_length=20, choices=Decision.choices, blank=True, null=True
    )
    date_evaluation = models.DateField(auto_now_add=True)

    # Champs ajoutés
    partage_avec_candidat = models.BooleanField(
        default=False,
        help_text=_("Indique si le feedback a été partagé au candidat"),
    )
    date_partage = models.DateTimeField(blank=True, null=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Évaluation")
        verbose_name_plural = _("Évaluations")
        db_table = "evaluation"
        ordering = ["-date_evaluation"]

    def __str__(self):
        return f"Évaluation de {self.entretien} - {self.get_decision_display() if self.decision else _('en cours')}"

    def get_absolute_url(self):
        return reverse("evaluation_detail", kwargs={"pk": self.pk})

    # Méthodes du diagramme
    def enregistrer(self):
        self.save()

    def calculer_note_globale(self):
        """Calcule la note globale à partir de la moyenne pondérée des critères d'évaluation."""
        criteres = self.criteres.all()
        if not criteres.exists():
            return None
        total_pondere = sum(
            (c.note / c.note_max) * c.poids for c in criteres if c.note_max
        )
        total_poids = sum(c.poids for c in criteres)
        note_sur_20 = round((total_pondere / total_poids) * 20, 2) if total_poids else None
        self.note_globale = note_sur_20
        self.save()
        return note_sur_20

    def partager_feedback(self):
        self.partage_avec_candidat = True
        self.date_partage = timezone.now()
        self.save()

    def modifier_decision(self, nouvelle_decision):
        self.decision = nouvelle_decision
        self.save()


class CritereEvaluation(models.Model):

    class Categorie(models.TextChoices):
        TECHNIQUE = "technique", _("Compétences techniques")
        COMPORTEMENTAL = "comportemental", _("Savoir-être / Comportemental")
        COMMUNICATION = "communication", _("Communication")
        CULTURE_ENTREPRISE = "culture", _("Adéquation culture d'entreprise")
        EXPERIENCE = "experience", _("Expérience professionnelle")
        AUTRE = "autre", _("Autre")

    # Relation "porte_sur" (1..*)
    evaluation = models.ForeignKey(
        "entretien.Evaluation",
        verbose_name=_("évaluation"),
        on_delete=models.CASCADE,
        related_name="criteres",
    )

    # Attributs du diagramme
    libelle = models.CharField(max_length=100)
    categorie = models.CharField(
        max_length=30, choices=Categorie.choices, default=Categorie.TECHNIQUE
    )
    note = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)])
    note_max = models.PositiveSmallIntegerField(
        default=20, validators=[MinValueValidator(1)]
    )
    commentaire = models.TextField(blank=True, null=True)

    # Champs ajoutés
    poids = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text=_("Poids du critère dans le calcul de la note globale"),
    )
    est_valide = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Critère d'évaluation")
        verbose_name_plural = _("Critères d'évaluation")
        db_table = "critere_evaluation"
        ordering = ["categorie", "libelle"]

    def __str__(self):
        return f"{self.libelle} ({self.note}/{self.note_max})"

    # Méthode du diagramme
    def valider(self):
        self.est_valide = True
        self.save()