from django.urls import path, include
from rest_framework import routers

from .views import RecipeViewSet, IngredientViewSet, UserProfileViewSet


router = routers.DefaultRouter()
router.register(r"recipes", RecipeViewSet)
router.register(r"ingredients", IngredientViewSet)
router.register(r"users", UserProfileViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
