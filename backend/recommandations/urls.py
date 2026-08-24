from rest_framwork.routers import DefaultRouter
from .views import (
    RecommandationViewSet
)

router = DefaultRouter()

router.register(r"recommendation", RecommandationViewSet, basename="recommendation")

urlpatterns = router.urls