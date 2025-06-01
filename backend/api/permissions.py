from rest_framework.permissions import BasePermission

from const.errors import ERROR_MESSAGES


class IsAuthorOrReadOnly(BasePermission):
    message = ERROR_MESSAGES["cant_edit"]

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.author == request.user
        return True
