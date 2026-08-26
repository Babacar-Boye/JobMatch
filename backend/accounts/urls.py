from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from . import views

router = DefaultRouter()
router.register(r'utilisateurs', views.UtilisateurViewSet, basename='utilisateur')
router.register(r'candidats', views.CandidatViewSet, basename='candidat')
router.register(r'recruteurs', views.RecruteurViewSet, basename='recruteur')
router.register(r'auth', views.AuthViewSet, basename='auth')
router.register(r"administrateurs", views.AdministrateurViewSet, basename="administrateur")

urlpatterns = [
    path('', include(router.urls)),

    # JWT natif SimpleJWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Reset password
    path('reinitialiser-password/demande/', views.DemandeReinitialisationView.as_view(), name='demande_reset'),
    path('reinitialiser-password/confirmer/', views.ConfirmerReinitialisationView.as_view(), name='confirmer_reset'),
]