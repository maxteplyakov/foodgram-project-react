from django_filters.rest_framework import FilterSet, CharFilter, filters
from .models import Ingredient, Recipe


# Несмотря на istartswith, почему-то это все равно работает регистрозависмо
class IngredientsFilter(FilterSet):

    name = CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ['name']


class RecipeFilter(FilterSet):
    author = filters.CharFilter(field_name="author__id", lookup_expr="exact")
    tags = filters.AllValuesMultipleFilter(field_name="tags__slug", lookup_expr="iexact")
    is_in_shopping_cart = filters.BooleanFilter(method="is_shopping_cart")
    is_favorited = filters.BooleanFilter(method="is_favorite")

    class Meta:
        model = Recipe
        fields = [
            "author",
            "tags",
            "is_in_shopping_cart",
            "is_favorited"
        ]

    def is_shopping_cart(self, queryset, name, value):
        if value is True:
            return queryset.filter(shopping_list__user=self.request.user)
        elif value is False:
            return queryset.exclude(shopping_list__user=self.request.user)
        return queryset

    def is_favorite(self, queryset, name, value):
        if value is True:
            return queryset.filter(favorited_by__user=self.request.user)
        elif value is False:
            return queryset.exclude(favorited_by__user=self.request.user)
        return queryset
