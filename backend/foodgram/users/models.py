from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(blank=False, unique=True)
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']
    USERNAME_FIELD = 'email'


class Subscription(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='subscribers'
    )
    subscriber = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='subscribed_to'
    )

    class Meta:
        constraints = [models.UniqueConstraint(
        fields=['author', 'subscriber'],
        name='unique_author_in_subscriptions'
        ), ]
        ordering = ['-author__username']
