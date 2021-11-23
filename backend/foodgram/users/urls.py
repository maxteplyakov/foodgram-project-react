from django.contrib.auth import get_user_model
from rest_framework.routers import DefaultRouter

from users.views import SubscriptionsViewSet, UserViewSet

router = DefaultRouter()
router.register("users/subscriptions",
                SubscriptionsViewSet, basename='subscriptions')
router.register("users", UserViewSet, basename='users')

User = get_user_model()

urlpatterns = router.urls
