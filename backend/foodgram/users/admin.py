from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import MyCustomUser, Subscriptions


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'subscriber',)


admin.site.register(MyCustomUser, UserAdmin)
