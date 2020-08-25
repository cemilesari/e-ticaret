# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from functools import wraps
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.contrib import messages
from rest_framework_jwt.settings import api_settings
from django.conf import settings
import time

def no_user(view=None):
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            try:
                if request.user.is_authenticated:
                    return redirect('/')               
            except Exception as e:
                pass
            return func(request, *args, **kwargs)
        return inner
    if view:
        return decorator(view)
    return decorator
