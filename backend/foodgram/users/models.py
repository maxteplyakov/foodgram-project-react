
from django.db import models
from django.contrib.auth.models import AbstractUser


class MyCustomUser(AbstractUser):
    is_subcribed = models.BooleanField(default=False)
    email = models.EmailField(blank=False, unique=True)

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']
    USERNAME_FIELD = 'email'

    def is_subscribed(self):
        return False

