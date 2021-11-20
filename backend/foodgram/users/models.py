from django.db import models
from django.contrib.auth.models import AbstractUser


class MyCustomUser(AbstractUser):
    email = models.EmailField(blank=False, unique=True)
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']
    USERNAME_FIELD = 'email'


class Subscriptions(models.Model):
    author = models.ForeignKey(
        MyCustomUser, on_delete=models.CASCADE, related_name='subscribers'
    )
    subscriber = models.ForeignKey(
        MyCustomUser, on_delete=models.CASCADE, related_name='subscribed_to'
    )

    class Meta:
        unique_together = ['author', 'subscriber']
        ordering = ['-author__username']
