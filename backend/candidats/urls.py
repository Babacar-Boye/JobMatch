from rest_framework.routers import DefaultRouter

from .views import (
    CVViewSet,
    ExperienceViewSet,
    CompetenceViewSet,
    FormationViewSet,
    PreferenceViewSet,
)

router = DefaultRouter()
router.register(r"cv", CVViewSet, basename="cv")
router.register(r"experiences", ExperienceViewSet, basename="experience")
router.register(r"competences", CompetenceViewSet, basename="competence")
router.register(r"formations", FormationViewSet, basename="formation")
router.register(r"preferences", PreferenceViewSet, basename="preference")

urlpatterns = router.urls

















# urlpatterns = [
#     # CV
#     path(
#         "cv/",
#         CVViewSet.as_view({"get": "list", "post": "create"}),
#         name="cv-list",
#     ),
#     path(
#         "cv/<int:pk>/",
#         CVViewSet.as_view({
#             "get": "retrieve",
#             "put": "update",
#             "patch": "partial_update",
#             "delete": "destroy",
#         }),
#         name="cv-detail",
#     ),

#     # Experience
#     path(
#         "experiences/",
#         ExperienceViewSet.as_view({"get": "list", "post": "create"}),
#         name="experience-list",
#     ),
#     path(
#         "experiences/<int:pk>/",
#         ExperienceViewSet.as_view({
#             "get": "retrieve",
#             "put": "update",
#             "patch": "partial_update",
#             "delete": "destroy",
#         }),
#         name="experience-detail",
#     ),

#     # Competence
#     path(
#         "competences/",
#         CompetenceViewSet.as_view({"get": "list", "post": "create"}),
#         name="competence-list",
#     ),
#     path(
#         "competences/<int:pk>/",
#         CompetenceViewSet.as_view({
#             "get": "retrieve",
#             "put": "update",
#             "patch": "partial_update",
#             "delete": "destroy",
#         }),
#         name="competence-detail",
#     ),

#     # Formation
#     path(
#         "formations/",
#         FormationViewSet.as_view({"get": "list", "post": "create"}),
#         name="formation-list",
#     ),
#     path(
#         "formations/<int:pk>/",
#         FormationViewSet.as_view({
#             "get": "retrieve",
#             "put": "update",
#             "patch": "partial_update",
#             "delete": "destroy",
#         }),
#         name="formation-detail",
#     ),

#     # Preference
#     path(
#         "preferences/",
#         PreferenceViewSet.as_view({"get": "list", "post": "create"}),
#         name="preference-list",
#     ),
#     path(
#         "preferences/<int:pk>/",
#         PreferenceViewSet.as_view({
#             "get": "retrieve",
#             "put": "update",
#             "patch": "partial_update",
#             "delete": "destroy",
#         }),
#         name="preference-detail",
#     ),
# ]