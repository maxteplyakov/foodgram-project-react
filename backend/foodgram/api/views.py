import time

from django.shortcuts import get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseNotFound
from django.db.models import Sum

from django.http import FileResponse

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly,
)

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


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer

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
            record = get_object_or_404(models.Favorite, user=user, recipe=recipe)
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
            record = get_object_or_404(models.ShoppingList, user=user, recipe=recipe)
            record.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False, methods=['GET'],
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = request.user
        filename = f'user_{user.id}_shopping_list_{time.strftime("%Y%m%d")}.txt'
        print(filename)
        user_recipes = []
        for recipe in models.ShoppingList.objects.filter(user=user):
            user_recipes.append(recipe.recipe_id)
        ingredients_amount = models.Ingredient.objects.filter(ingredientsinrecepie__recipe_id__in=user_recipes).annotate(total_amount=Sum('ingredientsinrecepie__amount'))
        print(ingredients_amount)

        for ingredient in ingredients_amount:
            print(f'{ingredient.name} ({ingredient.measurement_unit}) - {ingredient.total_amount} \n')

        fs = FileSystemStorage()
        # filename = 'mypdf.pdf'
        with open('media/'+filename, 'w') as file:
            for ingredient in ingredients_amount:
                file.write(f'{ingredient.name} ({ingredient.measurement_unit}) - {ingredient.total_amount} \n')

        if fs.exists(filename):
            with fs.open(filename) as file:
                response = HttpResponse(file, content_type='text/plain')
                response['Content-Disposition'] = f'attachment; filename={filename}'
                return response
        else:
            return HttpResponseNotFound('The requested pdf was not found in our server.')

        # response = FileResponse(open('media/'+filename, 'rb'), as_attachment=True, filename=filename)
        # return response




# class IngredientsInRecipeViewSet(viewsets.ReadOnlyModelViewSet):
#     # permission_classes = [IsAdmin | ReadOnly]
#     pagination_class = None
#     serializer_class = serializers.IngredientsInRecepieSerializer
#     queryset = models.IngredientsInRecepie.objects.all()
