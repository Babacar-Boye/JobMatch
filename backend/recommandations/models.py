from django.db import models
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Recommandation(models.Model):

    class Statut(models.TextChoices):
        NOUVELLE = "nouvelle", _("Nouvelle")
        VUE = "vue", _("Vue par le candidat")
        IGNOREE = "ignoree", _("Ignorée")
        POSTULEE = "postulee", _("A conduit à une candidature")

    candidat = models.ForeignKey(
        "account.Candidat",
        verbose_name=_("candidat"),
        on_delete=models.CASCADE,
        related_name="recommandations",
    )
    offre = models.ForeignKey(
        "offre.OffreEmploi",
        verbose_name=_("offre d'emploi"),
        on_delete=models.CASCADE,
        related_name="recommandations",
    )

    score_matching = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text=_("Score de compatibilité candidat/offre calculé par l'IA (0 à 100)"),
    )
    raison = models.TextField(
        blank=True, null=True,
        help_text=_("Explication générée par l'IA sur la pertinence de cette recommandation"),
    )

    statut = models.CharField(
        max_length=20, choices=Statut.choices, default=Statut.NOUVELLE
    )

    date_recommandation = models.DateTimeField(auto_now_add=True)
    date_consultation = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _("Recommandation")
        verbose_name_plural = _("Recommandations")
        db_table = "recommandation"
        ordering = ["-score_matching", "-date_recommandation"]
        unique_together = ("candidat", "offre")

    def __str__(self):
        return f"{self.offre} → {self.candidat} ({self.score_matching}%)"

    def get_absolute_url(self):
        return reverse("recommandation_detail", kwargs={"pk": self.pk})

    def marquer_vue(self):
        if self.statut == self.Statut.NOUVELLE:
            self.statut = self.Statut.VUE
            self.date_consultation = models.functions.Now()
            self.save(update_fields=["statut", "date_consultation"])