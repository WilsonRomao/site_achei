from rest_framework.permissions import BasePermission


class IsAdministrador(BasePermission):
    message = "Acesso negado. Perfil administrador necessário."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and "administrador" in (request.user.perfis or [])
        )
