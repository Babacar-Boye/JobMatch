from rest_framework.routers import DefaultRouter
from .views import (
    EntretienViewSet,
    EvaluationViewSet,
    CritereEvaluationViewSet,
)

router = DefaultRouter()

router.register(r"entretien", EntretienViewSet, basename="entretient")
router.register(r"evaluation", EvaluationViewSet, basename="evaluation")
router.register(r"critere_evaluation", CritereEvaluationViewSet, basename="critere_evaluation")

urlpatterns = router.urls