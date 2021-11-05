from rest_framework import serializers

from . import models


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
