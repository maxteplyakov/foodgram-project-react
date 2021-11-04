from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError

from djoser import utils
from djoser.compat import get_user_email, get_user_email_field_name
from djoser.conf import settings
from rest_framework.validators import UniqueValidator

from .models import MyCustomUser

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed'
        ]
        # fields = tuple(User.REQUIRED_FIELDS) + (
        #     settings.USER_ID_FIELD,
        #     settings.LOGIN_FIELD,
        # )
        # read_only_fields = (settings.LOGIN_FIELD,)

    # def update(self, instance, validated_data):
    #     email_field = get_user_email_field_name(User)
    #     if settings.SEND_ACTIVATION_EMAIL and email_field in validated_data:
    #         instance_email = get_user_email(instance)
    #         if instance_email != validated_data[email_field]:
    #             instance.is_active = False
    #             instance.save(update_fields=["is_active"])
    #     return super().update(instance, validated_data)


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, validators=[UniqueValidator(User.objects.all())])
    username = serializers.CharField(max_length=150, validators=[UniqueValidator(User.objects.all())])
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    password = serializers.CharField()

    default_error_messages = {
        "cannot_create_user": settings.CONSTANTS.messages.CANNOT_CREATE_USER_ERROR
    }

    class Meta:
        model = MyCustomUser
        # fields = tuple(User.REQUIRED_FIELDS) + (
        #     settings.LOGIN_FIELD,
        #     settings.USER_ID_FIELD,
        #     "password",
        #     "email"
        # )
        fields = ['email', 'id', 'username', 'first_name', 'last_name', 'password']

    read_only_fields = ['id'] #(settings.LOGIN_FIELD,)
    write_only_fields = ['password']
    # def validate(self, attrs):
    #     user = User(**attrs)
    #     password = attrs.get("password")
    #
    #     try:
    #         validate_password(password, user)
    #     except django_exceptions.ValidationError as e:
    #         serializer_error = serializers.as_serializer_error(e)
    #         raise serializers.ValidationError(
    #             {"password": serializer_error["non_field_errors"]}
    #         )
    #
    #     return attrs

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
            user = User.objects.create_user(**validated_data)
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
        return user


# class UserCreatePasswordRetypeSerializer(UserCreateSerializer):
#     default_error_messages = {
#         "password_mismatch": settings.CONSTANTS.messages.PASSWORD_MISMATCH_ERROR
#     }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["re_password"] = serializers.CharField(
#             style={"input_type": "password"}
#         )
#
#     def validate(self, attrs):
#         self.fields.pop("re_password", None)
#         re_password = attrs.pop("re_password")
#         attrs = super().validate(attrs)
#         if attrs["password"] == re_password:
#             return attrs
#         else:
#             self.fail("password_mismatch")
