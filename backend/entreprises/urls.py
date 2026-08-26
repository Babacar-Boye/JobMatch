from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import EnrteprisePublicViewSet, EntrepriseViewSet

router = DefaultRouter()

router.register(r'entreprise', EntrepriseViewSet, basename='entreprise')
router.register(r'entreprise_publique', EnrteprisePublicViewSet, basename='entreprise_publique')

urlpatterns = [
    path('', include(router.urls)),
]