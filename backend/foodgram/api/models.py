from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    color = models.CharField(max_length=7, blank=False, null=True, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, verbose_name='Название продукта')
    measurement_unit = models.CharField(max_length=200, blank=False, null=False, verbose_name='Единица измерения')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipies',  blank=False, null=False)
    name = models.CharField(max_length=200, blank=False, null=False, verbose_name='Название блюда')
    image = models.ImageField(upload_to='Recepies_pic/', blank=False, null=False, verbose_name='Изображение')
    text = models.TextField(max_length=2048, blank=False, null=False, verbose_name='Текстовое описание')
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientsInRecepie', through_fields=('recipe', 'ingredient'), blank=False)
    tags = models.ManyToManyField(Tag, blank=False)
    cooking_time = models.PositiveSmallIntegerField(blank=False, null=False, verbose_name='Время приготовления')
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class IngredientsInRecepie(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_amount')
    amount = models.PositiveSmallIntegerField(blank=False, null=False)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['ingredient', 'recipe'],
            name='unique_ingredient_in_recipe'
        ), ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorite_recipes'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorited_by'
    )

    class Meta:
        unique_together = ['user', 'recipe']


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes_in_shop_list'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shopping_list'
    )

    class Meta:
        unique_together = ['user', 'recipe']
