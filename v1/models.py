from enum import Enum
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """The user."""
    
    def __str__(self):
        return self.username
    pass
    
    class Meta:
      app_label = 'v1'

class Recipe(models.Model):
    """The recipe model"""

    name = models.CharField(
        max_length=255,
        help_text="The name of the recipe"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
      app_label = 'v1'

class Instruction(models.Model):
    """Instruction model, linked to Recipe"""
    
    id = models.BigAutoField(primary_key=True)
    step_number=models.PositiveIntegerField(
        default=0,
        help_text="Step order number"
    )
    description=models.CharField(
        max_length=500,
        help_text="Step instruction text"
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name="instructions",
        on_delete=models.CASCADE
    )

    class Meta:
      app_label = 'v1'
      ordering = ['step_number']
      unique_together = ['step_number', 'recipe']


class Ingredient(models.Model):
    """Ingredient model, linked to Recipe"""

    class Unit(models.TextChoices):
        """Unit type enumeration"""

        GRAMS = 'gr', _('Grams')
        KILOGRAMS = 'kg', _('Kilograms')
        TBS = 'tbs', _('Table Spoons')
        OZ = 'oz', _('Ounces')
        ML = 'mL', _('Milliliters')
    
    id = models.BigAutoField(primary_key=True)
    recipe = models.ForeignKey(
        Recipe,
        related_name="ingredients",
        on_delete=models.CASCADE
    )
    ingredient_name = models.CharField(
        max_length=100,
        help_text="ingredient name"
    )
    amount = models.FloatField(default=0)
    unit = models.CharField(
        max_length=10,
        choices=Unit.choices,
        null=False,
        blank=False
    )
    
    class Meta:
      app_label = 'v1'