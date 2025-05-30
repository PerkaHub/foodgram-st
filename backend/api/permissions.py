from rest_framework.permissions import BasePermission

CANT_EDIT = "Вы не можете изменять чужие рецепты"


class IsAuthorOrReadOnly(BasePermission):
    message = CANT_EDIT

    def has_object_permission(self, request, view, obj):
        # Разрешение только автору для изменения
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.author == request.user
        return True
