from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyCustomUser

admin.site.register(MyCustomUser, UserAdmin)