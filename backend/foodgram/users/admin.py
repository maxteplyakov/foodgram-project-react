from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Subscription


@admin.register(Subscription)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'subscriber',)


@admin.register(CustomUser)
class SubscriptionsAdmin(UserAdmin):
    list_display = ('pk', 'email', 'username', 'first_name', 'last_name')
    list_filter = ('email', 'username')
