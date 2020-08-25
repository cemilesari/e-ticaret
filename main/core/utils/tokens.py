# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.conf import settings

class EmailActiveTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.email) + six.text_type(user.role) + 
            six.text_type(user.last_name) + six.text_type(user.first_name)
        )

email_active_token = EmailActiveTokenGenerator()


class RestPassswordTokenGenertorclass(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.email) + six.text_type(user.role) + 
            six.text_type(user.last_name) + six.text_type(settings.SECRET_KEY) + six.text_type(timestamp)
        )

reset_password_token = RestPassswordTokenGenertorclass()
