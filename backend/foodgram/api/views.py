from rest_framework import viewsets
from . import serializers, models
from .filters import IngredientsFilter


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    # permission_classes = [IsAdmin | ReadOnly]
    pagination_class = None
    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    # permission_classes = [IsAdmin | ReadOnly]
    pagination_class = None
    serializer_class = serializers.IngredientSerializer
    queryset = models.Ingredient.objects.all()
    # filter_backends = (DjangoFilterBackend,)
    filter_class = IngredientsFilter
