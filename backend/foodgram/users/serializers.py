from django.contrib.auth import get_user_model
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction
from djoser.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import CustomUser, Subscription

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.SerializerMethodField(read_only=True)
    email = serializers.EmailField(read_only=True)
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed'
        ]

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        return request.user.is_authenticated and Subscription.objects.filter(
            author=obj, subscriber=request.user
        ).exists()


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254, validators=[UniqueValidator(User.objects.all())]
    )
    username = serializers.CharField(
        max_length=150, validators=[UniqueValidator(User.objects.all())]
    )
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    default_error_messages = {
        "cannot_create_user": settings.CONSTANTS.messages.CANNOT_CREATE_USER_ERROR
    }

    class Meta:
        model = CustomUser
        fields = [
            'email', 'id', 'username', 'first_name', 'last_name', 'password'
        ]

    read_only_fields = ['id']
    write_only_fields = ['password']

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(serializer_error)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = CustomUser.objects.create_user(**validated_data)
        return user
