# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six



class DeviceTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.email) + six.text_type(user.pin) + six.text_type(user.username)
        )


class RestPassswordTokenGenertorclass(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.email) + six.text_type(user.role) + 
            six.text_type(user.last_name) + six.text_type(settings.SECRET_KEY) + six.text_type(timestamp)
        )

reset_password_token = RestPassswordTokenGenertorclass()


class EmailActiveTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.email) + six.text_type(user.username) + six.text_type(user.main_key)
        )