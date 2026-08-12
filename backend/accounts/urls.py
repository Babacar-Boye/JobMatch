# urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import DemandeReinitialisationView, ConfirmerReinitialisationView, UtilisateurViewSet, CandidatViewSet, DeconnexionView

router = DefaultRouter()
router.register(
    "utilisateurs",
    UtilisateurViewSet,
    basename="utilisateur"
)

router.register(
    "candidats",
    CandidatViewSet,
    basename="candidat"
)
urlpatterns = router.urls
urlpatterns = [
    
    path('mot-de-passe/reinitialiser/', DemandeReinitialisationView.as_view(), name='demande-reinitialisation'),
    path('mot-de-passe/confirmer/', ConfirmerReinitialisationView.as_view(), name='confirmer-reinitialisation'),
]