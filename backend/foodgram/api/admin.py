from django.contrib import admin
from . import models


@admin.register(models.Tag)
class RecepieAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


@admin.register(models.Ingredient)
class RecepieAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')


@admin.register(models.IngredientsInRecepie)
class RecepieAdmin(admin.ModelAdmin):
    list_display = ('recepie', 'ingredient', 'amount')


@admin.register(models.Recepie)
class RecepieAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'text', 'cooking_time', 'pub_date')
    list_filter = ('author',)

