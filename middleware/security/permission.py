from rest_framework.permissions import BasePermission

from backoffice import models


class Mediapp_bePermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user:
            return False
        user_login_code = request.user.get('user_login_code')
        user_login = models.UserLogin.objects.get_user_by_code(user_login_code)
        return bool(user_login)
