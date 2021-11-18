from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Count

from . import models
from users.serializers import UserSerializer
import users


User = get_user_model()

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tag
        fields = '__all__'
        read_only_fields = ['name', 'color', 'slug']


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
        fields = ['id', 'name', 'measurement_unit', 'amount']


class CreateIngredientsInRecepieSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = models.IngredientsInRecepie
        fields = ['id', 'amount']


class FavoriteSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = Base64ImageField(source='recipe.image', required=False)
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = models.Favorite
        fields = ['id', 'name', 'image', 'cooking_time', 'user', 'recipe']
        extra_kwargs = {
            'user': {'write_only': True},
            'recipe': {'write_only': True}
        }


class ShoppingListSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = Base64ImageField(source='recipe.image', required=False)
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = models.ShoppingList
        fields = ['id', 'name', 'image', 'cooking_time', 'user', 'recipe']
        extra_kwargs = {
            'user': {'write_only': True},
            'recipe': {'write_only': True}
        }


class SubscriptionRecipesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Recipe
        fields = ['id', 'name', 'image', 'cooking_time']


class RecipeSerializer(serializers.ModelSerializer):

    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    ingredients = CreateIngredientsInRecepieSerializer(
        source='recipe_amount',
        many=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=models.Tag.objects.all(),
        many=True
    )
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time"
        )
        model = models.Recipe

    def to_representation(self, obj):
        """."""
        self.fields['tags'] = TagSerializer(many=True)
        self.fields['ingredients'] = IngredientsInRecepieSerializer(source='recipe_amount', many=True)
        return super().to_representation(obj)

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get("request")
        if request.user.is_authenticated and models.ShoppingList.objects.filter(recipe=obj, user=request.user).exists():
            return True
        return False

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if request.user.is_authenticated and models.Favorite.objects.filter(recipe=obj, user=request.user).exists():
            return True
        return False

    def create(self, validated_data):

        ingredients_data = validated_data.pop("recipe_amount")
        tags_data = validated_data.pop("tags")
        recipe = models.Recipe.objects.create(**validated_data)
        recipe.tags.set(tags_data)
        for item in ingredients_data:
            current_ingredient = get_object_or_404(models.Ingredient, id=dict(item)["id"])
            models.IngredientsInRecepie.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=item["amount"]
            )
        return recipe

    def update(self, instance, validated_data):
        """Recipe update."""
        ingredients_data = validated_data.pop("recipe_amount")
        ingredients = (instance.recipe_amount).all()
        ingredients = list(ingredients)
        tags_data = validated_data.pop("tags")
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        instance.tags.clear()
        instance.tags.set(tags_data)
        instance.save()
        instance.ingredients.clear()
        for item in ingredients_data:
            current_ingredient = get_object_or_404(models.Ingredient, id=dict(item)["id"])
            models.IngredientsInRecepie.objects.create(
                ingredient=current_ingredient,
                recipe=instance,
                amount=item["amount"]
            )
        return instance


class SubscriptionSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    first_name = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = SubscriptionRecipesSerializer(many=True, source='recipies', read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = users.models.Subscriptions
        fields = [
            'email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed', 'recipes', 'recipes_count'
        ]
        extra_kwargs = {
            'author': {'write_only': True},
            'subscriber': {'write_only': True}
        }

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request.user.is_authenticated and users.models.Subscriptions.objects.filter(
                author=obj, subscriber=request.user
        ).exists():
            return True
        return False

    def get_recipes_count(self, obj):
        return models.Recipe.objects.filter(author=obj).count()

    def validate(self, data):
        request = self.context['request']
        author = User.objects.get(pk=self.initial_data['author'])
        if request._request.method == 'GET':
            if users.models.Subscriptions.objects.filter(author=author, subscriber=request.user).exists():
                raise serializers.ValidationError('Вы уже подписаны на этого автора')
            if author == request.user:
                raise serializers.ValidationError('Вы не можете подписаться на себя')
        self.initial_data['id'] = author.id
        return data
    # recipes = serializers.SerializerMethodField(read_only=True)
    #
    # def get_recipes(self, obj):
    #     request = self.context.get("request")
    #     if request.user.is_authenticated and Subscriptions.objects.filter(author=obj, subscriber=request.user).exists():
    #         return True
    #     return False

# class RecipeSerializer(serializers.ModelSerializer):
#     ingredients = IngredientsInRecepieSerializer(source='ingredientsinrecepie_set', many=True)
#     tags = TagSerializer(many=True)
#     author = UserSerializer()
#
#     class Meta:
#         model = models.Recipe
#         fields = '__all__'
#
#
# class CreateRecipeSerializer(serializers.ModelSerializer):
#
#     image = Base64ImageField()
#     author = UserSerializer(read_only=True)
#     ingredients = serializers.SerializerMethodField()
#     tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#
#     class Meta:
#         fields = (
#             "id",
#             "tags",
#             "author",
#             "ingredients",
#             "image",
#             "name",
#             "text",
#             "cooking_time"
#         )
#         model = models.Recipe
#
#
#     def get_ingredients(self, obj):
#         return obj.ingredients
#
#     def create(self, validated_data):
#         """."""
#         print(validated_data)
#         ingredients = validated_data.pop("ingredients")
#         recipe = models.Recipe.objects.create(**validated_data)
#         for ingredient in ingredients:
#             print(ingredient)
#             print(ingredient.get("id"))
#             print(recipe)
#             print(ingredient.get("amount"))
#             models.IngredientsInRecepie.objects.create(
#                 ingredient=ingredient.get("id"),
#                 recipe=recipe,
#                 amount=ingredient.get("amount")
#             )
#         return recipe

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
