from rest_framework.routers import DefaultRouter
from .views import (
    CandidatureViewSet,
    PieceJointeViewSet
)


router = DefaultRouter()

router.register(r"candidature", CandidatureViewSet, basename="candidature")
router.register(r"piece_jointe", PieceJointeViewSet, basename="piece_jointe")

urlpatterns = router.urls