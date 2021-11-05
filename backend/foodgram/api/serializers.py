from rest_framework import serializers

from . import models
from users.serializers import UserSerializer

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tag
        fields = '__all__'
        # exclude = ['id']
        # lookup_field = 'slug'
        # extra_kwargs = {
        #     'url': {'lookup_field': 'slug'}
        # }


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Ingredient
        fields = '__all__'


class IngredientsInRecepieSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')


    class Meta:
        model = models.IngredientsInRecepie
        fields = ['id', 'name', 'measurement_unit']





class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientsInRecepieSerializer(many=True)
    tags = TagSerializer(many=True)
    author = UserSerializer()

    class Meta:
        model = models.Recipe
        fields = '__all__'

    # def create(self, validated_data):
    #     """."""
    #     ingredients = validated_data.pop("ingredients")
    #     recipe = Recipe.objects.create(**validated_data)
    #     for ingredient in ingredients:
    #         IngredientAmount.objects.create(
    #             ingredient=ingredient.get("id"),
    #             recipe=recipe,
    #             amount=ingredient.get("amount")
    #         )
    #     return recipe



# class MembershipSerializer(serializers.HyperlinkedModelSerializer):
#
#     id = serializers.Field(source='group.id')
#     name = serializers.Field(source='group.name')
#
#     class Meta:
#         model = Membership
#
#         fields = ('id', 'name', 'join_date', )


# class IngredientSerializer(serializers.ModelSerializer):
#     """Serializer for the Ingredient model."""
#     class Meta:
#         fields = ("id", "name", "measurement_unit")
#         model = Ingredient
# ​
# ​
# class IngredientAmountSerializer(serializers.ModelSerializer):
#     """Serializer for the IngredientAmount model."""
#     class Meta:
#         # fields = ("id", "name", "measurement_unit", "amount")
#         fields = ("id", "amount")
#         model = IngredientAmount
# ​
# ​
# class RecipeSerializer(serializers.ModelSerializer):
#     """Serializer for the Recipe model."""
#     image = Base64ImageField()
#     author = UserSerializer(read_only=True)
#     ingredients = IngredientAmountSerializer(many=True)
# ​
#     class Meta:
#         fields = (
#             "id",
#             # "tags",
#             "author",
#             "ingredients",
#             "image",
#             "name",
#             "text",
#             "cooking_time"
#         )
#         model = Recipe
# ​
#     def create(self, validated_data):
#         """."""
#         ingredients = validated_data.pop("ingredients")
#         recipe = Recipe.objects.create(**validated_data)
#         for ingredient in ingredients:
#             IngredientAmount.objects.create(
#                 ingredient=ingredient.get("id"),
#                 recipe=recipe,
#                 amount=ingredient.get("amount")
#             )
#         return recipe
