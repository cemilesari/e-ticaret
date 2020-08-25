from __future__ import unicode_literals
from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured
from django.apps import apps
from django.contrib.auth.hashers import check_password

from main.users.models import User

class UserModelBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        try:
            user = self.user_class.objects.get(username=username)
            if user.check_password(password):
                return user
        except self.user_class.DoesNotExist:
            #log that
            return None

    def get_user(self, user_id):
        try:
            return self.user_class.objects.get(pk=user_id)
        except self.user_class.DoesNotExist:
            #log that
            return None

    @property
    def user_class(self):
        if not hasattr(self, '_user_class'):
            self._user_class = apps.get_model(*settings.AUTH_USER_MODEL.split('.', 2))
            if not self._user_class:
                raise ImproperlyConfigured('Could not get auth user model')
        return self._user_class

def lang_authenticate(username=None, password=None):
    try:
        if username and password:
            if '@' in username:
                kwargs = {'email': username}
            else:
                kwargs = {'username': username}
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
    except:
        return None