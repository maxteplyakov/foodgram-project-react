from rest_framework import permissions


class IsAuthorOrReadONly (permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print("getting_Permission")
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (request.user == obj.author)
