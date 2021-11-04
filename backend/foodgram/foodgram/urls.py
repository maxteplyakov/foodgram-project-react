from django.contrib import admin
from django.urls import include, path, re_path


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'api/auth/', include('djoser.urls.authtoken')),
    re_path(r'api/', include('users.urls')),
]