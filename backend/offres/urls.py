from rest_framwork.routers import DefaultRouter
from .views import (
    OffreEmploiCreateUpdateViewSet,
    OffreEmploiListViewSet,
    OffreEmploiDetailViewSet,
)

router = DefaultRouter()

router.register(r"liste_offre", OffreEmploiListViewSet, basename="liste_offre")
router.register(r"detail_offre", OffreEmploiDetailViewSet, basename="detail_offre")
router.register(r"creation_edition_offre", OffreEmploiCreateUpdateViewSet, basename="creation_edition_offre")

urlpatterns = router.urls