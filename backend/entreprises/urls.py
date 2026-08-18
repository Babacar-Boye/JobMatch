from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from . import views

router = DefaultRouter()

router.register(r'entreprise', views.EntrepriseViewSet, basename='entreprise')
router.register(r'entreprise_publique', views.EntreprisePublicSerializer, basename='entreprise_publique')

urlpatterns = [
    path('', include(router.urls)),
]