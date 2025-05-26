from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    IngredientViewSet,
    RecipeViewSet,
    SubscriptionViewSet,
    TagViewSet,
)

app_name = "api"

router = DefaultRouter()
router.register("ingredients", IngredientViewSet, basename="ingredients")
router.register("recipes", RecipeViewSet, basename="recipes")
router.register("tags", TagViewSet, basename="tags")

urlpatterns = [
    path("users/subscriptions/",
         SubscriptionViewSet.as_view({"get": "list"}),
         name="subscriptions"),
    path("", include(router.urls)),
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
