from django.db import models
from django.utils import timezone


class Entretien(models.Model):
    """
    Représente un entretien planifié avec un candidat.
    Relation 1-1 avec Evaluation (faire_objet) :
    un Entretien donne lieu à une Evaluation.
    """

    FORMAT_CHOICES = [
        ("presentiel", "Présentiel"),
        ("visio", "Visioconférence"),
        ("telephonique", "Téléphonique"),
    ]

    STATUT_CHOICES = [
        ("planifie", "Planifié"),
        ("confirme", "Confirmé"),
        ("annule", "Annulé"),
        ("termine", "Terminé"),
        ("reprogramme", "Reprogrammé"),
    ]

    id = models.AutoField(primary_key=True)
    format = models.CharField(max_length=50, choices=FORMAT_CHOICES)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default="planifie")
    lienVisio = models.CharField(max_length=255, blank=True, null=True)
    adresseLieu = models.CharField(max_length=255, blank=True, null=True)
    rappelEnvoye = models.BooleanField(default=False)
    noteRecruteur = models.CharField(max_length=255, blank=True, null=True)
    dateHeure = models.DateTimeField()
    dateCreation = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Entretien"
        verbose_name_plural = "Entretiens"
        ordering = ["-dateHeure"]

    def __str__(self):
        return f"Entretien #{self.id} - {self.format} - {self.statut}"

    # ---- Méthodes métier ----

    def planifier(self):
        """Planifie l'entretien (définit le statut initial)."""
        self.statut = "planifie"
        self.save()

    def confirmer(self):
        """Confirme l'entretien."""
        self.statut = "confirme"
        self.save()

    def annuler(self):
        """Annule l'entretien."""
        self.statut = "annule"
        self.save()

    def reprogrammer(self, nouvelle_date):
        """Reprogramme l'entretien à une nouvelle date/heure."""
        self.dateHeure = nouvelle_date
        self.statut = "reprogramme"
        self.save()

    def envoyerRappel(self):
        """Envoie un rappel au candidat/recruteur."""
        # logique d'envoi (email/notification) à implémenter
        self.rappelEnvoye = True
        self.save()

    def terminer(self):
        """Marque l'entretien comme terminé."""
        self.statut = "termine"
        self.save()

    def genererLienVisio(self):
        """Génère (ou régénère) le lien de visioconférence."""
        # logique de génération de lien (ex: appel API Zoom/Meet)
        self.lienVisio = f"https://visio.example.com/entretien-{self.id}"
        self.save()
        return self.lienVisio


class Evaluation(models.Model):
    """
    Représente l'évaluation issue d'un Entretien.
    Relation 1-1 avec Entretien (faire_objet).
    Relation 1 à N avec CritereEvaluation (porte_sur).
    """

    DECISION_CHOICES = [
        ("favorable", "Favorable"),
        ("defavorable", "Défavorable"),
        ("en_attente", "En attente"),
    ]

    id = models.AutoField(primary_key=True)
    entretien = models.OneToOneField(
        Entretien,
        on_delete=models.CASCADE,
        related_name="evaluation",
        verbose_name="Entretien concerné",
    )
    noteGlobale = models.IntegerField(blank=True, null=True)
    commentaireGlobale = models.TextField(blank=True, null=True)
    pointForts = models.TextField(blank=True, null=True)
    pointAmeliorer = models.TextField(blank=True, null=True)
    decision = models.CharField(max_length=50, choices=DECISION_CHOICES, default="en_attente")
    dateEvaluation = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Evaluation"
        verbose_name_plural = "Evaluations"
        ordering = ["-dateEvaluation"]

    def __str__(self):
        return f"Evaluation #{self.id} - Entretien #{self.entretien_id}"

    # ---- Méthodes métier ----

    def Enregistrer(self):
        """Enregistre l'évaluation."""
        self.save()

    def calculerNoteGlobale(self):
        """Calcule la note globale à partir des critères associés."""
        criteres = self.criteres.all()
        if not criteres.exists():
            self.noteGlobale = None
        else:
            total = sum(c.note for c in criteres)
            total_max = sum(c.noteMax for c in criteres)
            self.noteGlobale = round((total / total_max) * 100) if total_max else 0
        self.save()
        return self.noteGlobale

    def partagerFeedback(self):
        """Partage le feedback (points forts / à améliorer) au candidat ou à l'équipe."""
        # logique d'envoi/partage à implémenter (email, notification, etc.)
        pass

    def modifierDecision(self, nouvelle_decision):
        """Modifie la décision finale de l'évaluation."""
        if nouvelle_decision in dict(self.DECISION_CHOICES):
            self.decision = nouvelle_decision
            self.save()
        return self.decision


class CritereEvaluation(models.Model):
    """
    Représente un critère d'évaluation associé à une Evaluation.
    Relation N à 1 avec Evaluation (porte_sur) : 1..* CritereEvaluation pour 1 Evaluation.
    """

    id = models.AutoField(primary_key=True)
    evaluation = models.ForeignKey(
        Evaluation,
        on_delete=models.CASCADE,
        related_name="criteres",
        verbose_name="Evaluation associée",
    )
    libelle = models.CharField(max_length=255)
    categorie = models.CharField(max_length=100, blank=True, null=True)
    note = models.IntegerField()
    noteMax = models.IntegerField(default=10)
    commentaire = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Critère d'évaluation"
        verbose_name_plural = "Critères d'évaluation"

    def __str__(self):
        return f"{self.libelle} ({self.note}/{self.noteMax})"

    # ---- Méthodes métier ----

    def valider(self):
        """Valide le critère (ex: vérifie que la note ne dépasse pas noteMax)."""
        if self.note > self.noteMax:
            raise ValueError("La note ne peut pas dépasser la note maximale.")
        self.save()
        return True