
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from v1.serializers import RecipeSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from v1.models import Recipe
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated

class RecipeViewSet(viewsets.ModelViewSet):
    """The basic CRUD operations for recipe model"""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
