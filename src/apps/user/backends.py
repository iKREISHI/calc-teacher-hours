from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class CustomAuthBackend(ModelBackend):
    """
    Custom authentication backend that allows login with username
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
            
        try:
            # Try to find user by username
            user = User.objects.get(Q(username=username))
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            # In case there are multiple users with same username
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None