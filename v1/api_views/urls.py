from django.urls import path, include
from rest_framework import routers
from .recipes import RecipeViewSet

router = routers.DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename="recipes")

urlpatterns = [
    path('', include(router.urls))
]
