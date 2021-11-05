from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    color = models.CharField(max_length=7, blank=False, null=True)
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

class Recepie(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipies',  blank=False, null=False)
    name = models.CharField(max_length=200, blank=False, null=False, verbose_name='Название блюда')
    image = models.ImageField(upload_to='Recepies_pic/', blank=False, null=False, verbose_name='Изображение')
    text = models.TextField(max_length=2048, blank=False, null=False, verbose_name='Текстовое описание')
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientsInRecepie', through_fields=('recepie', 'ingredient'), blank=False)
    tags = models.ManyToManyField(Tag, blank=False)
    cooking_time = models.PositiveSmallIntegerField(blank=False, null=False, verbose_name='Время приготовления')
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class IngredientsInRecepie(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recepie = models.ForeignKey(Recepie, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(blank=False, null=False)





# class Group(models.Model):
#     title = models.CharField(max_length=200)
#     slug = models.SlugField(unique=True, max_length=100)
#     description = models.TextField()
#
#     def __str__(self):
#         return self.title
#
#
#
#
# class Comment(models.Model):
#     post = models.ForeignKey(
#         Post, on_delete=models.CASCADE, related_name='comments',
#         blank=True, null=True, verbose_name='Пост'
#     )
#     author = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='comments',
#         verbose_name='Автор комментария'
#     )
#     text = models.TextField(verbose_name='Текст комментария')
#     created = models.DateTimeField('date created', auto_now_add=True)
#
#     class Meta:
#         ordering = ['-created']
#
#     def __str__(self):
#         return self.text
#
#     def post_id(self):
#         return self.post.id
#
#
# class Follow(models.Model):
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='follower'
#     )
#     author = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='following'
#     )
#
#     class Meta:
#         unique_together = ['user', 'author']
