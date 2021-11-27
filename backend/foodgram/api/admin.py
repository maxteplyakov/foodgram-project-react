from django.contrib import admin

from . import models


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(models.IngredientsInRecepie)
class IngredientsInRecepieAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'text', 'cooking_time', 'pub_date')
    list_filter = ('author', 'name', 'tags')


@admin.register(models.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user',)


@admin.register(models.ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user',)