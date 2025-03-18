from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import Usuario  # Usa el modelo abstracto principal

class AliasBackend(BaseBackend):
    def authenticate(self, request, alias=None, password=None, **kwargs):
        try:
            user = Usuario.objects.get(alias=alias)
            if user.check_password(password):
                return user
        except Usuario.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None