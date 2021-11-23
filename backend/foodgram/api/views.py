import time

from django.core.files.storage import FileSystemStorage
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.paginators import CustomPageSizePagination

from . import models, permissions, serializers
from .filters import IngredientsFilter, RecipeFilter


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    serializer_class = serializers.IngredientSerializer
    queryset = models.Ingredient.objects.all()
    filter_class = IngredientsFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    pagination_class = CustomPageSizePagination
    filter_class = RecipeFilter
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated]
        elif self.action in ("update", "destroy"):
            self.permission_classes = [permissions.IsAuthorOrReadONly]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True, methods=['GET', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(models.Recipe, pk=pk)
        if request.method == 'GET':
            data = {
                'user': user.id,
                'recipe': recipe.id
            }
            serializer = serializers.FavoriteSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            models.Favorite.objects.create(user=user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            record = get_object_or_404(
                models.Favorite, user=user, recipe=recipe
            )
            record.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True, methods=['GET', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(models.Recipe, pk=pk)
        if request.method == 'GET':
            data = {
                'user': user.id,
                'recipe': recipe.id
            }
            serializer = serializers.ShoppingListSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            models.ShoppingList.objects.create(user=user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            record = get_object_or_404(
                models.ShoppingList, user=user, recipe=recipe
            )
            record.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False, methods=['GET'],
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = request.user
        filename = f'user_{user.id}_shoppinglist_{time.strftime("%Y%m%d")}.txt'
        user_recipes = models.ShoppingList.objects.filter(
            user=user
        ).values_list('recipe_id')
        ingredients_amount = models.Ingredient.objects.filter(
            ingredientsinrecepie__recipe_id__in=user_recipes
        ).annotate(total_amount=Sum('ingredientsinrecepie__amount'))

        lines = []
        for ingredient in ingredients_amount:
            lines.append(
                f'{ingredient.name} ({ingredient.measurement_unit})'
                f' - {ingredient.total_amount} \n'
            )
        response_content = ''.join(lines)
        response = HttpResponse(
            response_content, content_type="text/plain,charset=utf8"
        )
        response['Content-Disposition'] = 'attachment; filename={0}'.format(
            filename
        )
        return response
