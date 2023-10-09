from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q


class PhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(Q(username=username) | Q(profile_user__phone=username))
        except user_model.DoesNotExist:
            return None
        except MultipleObjectsReturned:
            return None

        if user.check_password(password):
            return user
