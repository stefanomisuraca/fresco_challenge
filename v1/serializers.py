from rest_framework import serializers
from v1.models import Recipe, Instruction, Ingredient
from django.db.utils import IntegrityError
from typing import Dict

class InstructionSerializer(serializers.ModelSerializer):
    """Instruction api serilizer"""
    id = serializers.IntegerField(read_only=False, required=False)
    step_number = serializers.IntegerField(required=True)

    class Meta:
        model = Instruction
        exclude = ["recipe"]

class IngredientSerializer(serializers.ModelSerializer):
    """Ingredient api serializer"""
    id = serializers.IntegerField(read_only=False, required=False)
    amount = serializers.FloatField(required=True)

    class Meta:
        model = Ingredient
        exclude = ["recipe"]

class RecipeSerializer(serializers.ModelSerializer):

    name = serializers.CharField()
    instructions = InstructionSerializer(many=True, read_only=False)
    ingredients = IngredientSerializer(many=True)

    def create(self, validated_data:Dict) -> Recipe:
        """Custom create function for nested object Recipe"""
        recipe = Recipe.objects.create(
            name=validated_data.get("name")
        )
        for instruction in validated_data.get("instructions"):
            Instruction.objects.get_or_create(**instruction, recipe=recipe)
        for ingredient in validated_data.get("ingredients"):
            Ingredient.objects.get_or_create(**ingredient, recipe=recipe) 

        return recipe


    def update(self, instance:Recipe, validated_data:Dict) -> Recipe:
        """Custom update function for nested object Recipe"""
       
        # Handle Update or Create records instructions
        instance.name = validated_data.get("name")
        instructions_set = validated_data.pop("instructions")
        current_instructions_ids = [instance.id for instance in instance.instructions.all()]
        instructions_set_ids = [instruction.get("id") for instruction in instructions_set]
        
        for instruction in instructions_set:
            try:
                Instruction.objects.update_or_create(
                    id=instruction.get("id"),
                    step_number=instruction.get("step_number"),
                    defaults={**instruction, "recipe":instance}
                )
            except IntegrityError:
                print("Duplicate entry")
                continue
       
        # Handle Delete records instructions
        for instruction_id in current_instructions_ids:
            if instruction_id not in instructions_set_ids:
                print(instance.instructions.get(id=instruction_id))
                instance.instructions.get(id=instruction_id).delete()
        
        # Handle Update records Ingredients
        ingredients_set = validated_data.pop("ingredients")
        print(ingredients_set)
        current_ingredients_ids = [instance.id for instance in instance.ingredients.all()]
        ingredients_set_ids = [ingredient.get("id") for ingredient in ingredients_set]
        
        for ingredient in ingredients_set:
            try:
                obj, created = Ingredient.objects.update_or_create(
                    id=ingredient.get("id"),
                    # ingredient_name=ingredient.get("ingredient_name"),
                    # amount=ingredient.get("amount"),
                    # unit=ingredient.get("unit"),
                    defaults={**ingredient, "recipe":instance},
                )
                print(obj, created)
            except IntegrityError:
                print("Duplicate entry")
                continue
        
        # Handle Delete records ingredients
        for ingredient_id in current_ingredients_ids:
            if ingredient_id not in ingredients_set_ids:
                instance.ingredients.get(id=ingredient_id).delete()
       
        
        instance.save()
        return instance

    class Meta:
        model = Recipe
        fields = "__all__"