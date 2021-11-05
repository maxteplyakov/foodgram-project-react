from django_filters.rest_framework import FilterSet, CharFilter
from .models import Ingredient


# Несмотря на istartswith, почему-то это все равно работает регистрозависмо
class IngredientsFilter(FilterSet):

    name = CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ['name']
