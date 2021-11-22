from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from djoser.conf import settings
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api import serializers as api_serializers

from .models import Subscriptions
from .paginators import CustomPageSizePagination
from .serializers import UserCreateSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = settings.SERIALIZERS.user
    queryset = User.objects.all()
    permission_classes = settings.PERMISSIONS.user
    token_generator = default_token_generator
    lookup_field = settings.USER_ID_FIELD

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        # if settings.HIDE_USERS and self.action == "list" and not user.is_staff:
        #     queryset = queryset.filter(pk=user.pk)
        return queryset

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = settings.PERMISSIONS.user_create
        elif self.action == "list":
            self.permission_classes = settings.PERMISSIONS.user_list
        elif self.action == "set_password":
            self.permission_classes = settings.PERMISSIONS.set_password
        elif self.action == "destroy" or self.action == "me":
            self.permission_classes = settings.PERMISSIONS.user_delete
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        elif self.action == "set_password":
            return settings.SERIALIZERS.set_password
        elif self.action == "me":
            return settings.SERIALIZERS.current_user
        return self.serializer_class

    def get_instance(self):
        return self.request.user

    @action(["get"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)

    @action(["post"], detail=False)
    def set_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True, methods=['GET', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        subscriber = request.user
        author = get_object_or_404(User, pk=id)
        if request.method == 'GET':
            data = {
                'author': author.id,
                'subscriber': subscriber.id
            }
            serializer = api_serializers.SubscriptionSerializer(author, data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                Subscriptions.objects.create(author=author, subscriber=subscriber)

                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            record = get_object_or_404(Subscriptions, author=author, subscriber=subscriber)
            record.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = api_serializers.CurrentUserSubscriptionSerializer
    pagination_class = CustomPageSizePagination

    def get_queryset(self):
        return Subscriptions.objects.filter(subscriber=self.request.user)
