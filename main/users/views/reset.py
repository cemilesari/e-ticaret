# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render,redirect
from django.db.models import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib import messages
from django.urls import reverse

from main.users.models import User
from main.users.forms import ResetPasswordForm, ResetPasswordConfirmForm
from main.core.noify import send_password_rest_email
from main.core.tokens import reset_password_token
from main.core.utils import  display_form_validations

def request_reset_password(request):
    if request.POST:
        form = ResetPasswordForm(request.POST)
        username = request.POST.get("username")
        try:
            if form.is_valid():
                user = User.objects.get(Q(username=username)|Q(email=username))
                if user and send_password_rest_email(user.id):
                    messages.success(request, _("Success, Reset Password has been sent!"))
                    return redirect(reverse("users:login"))
            else:
                display_form_validations(form=form, request=request)
        except Exception as e:
            messages.error(request, _("Error, An error occured while sending reset password"))
    return render(request, "registration/reset.html")

def change_password_from_email(request, uidb64=None, token=None):
    resmessage, show_form = None, False
    user = None
    try:
        uid  = force_text(urlsafe_base64_decode(request.resolver_match.kwargs.get("uidb64")))
        user = User.objects.get(pk=uid)
        show_form = True
    except User.DoesNotExist:
        messages.error(request, _("Error, User does not match"))
    except (TypeError, ValueError, OverflowError):
        messages.error(request, _("Error, Unknown error occured, please reset password and try again."))
    if request.POST:
        form = ResetPasswordConfirmForm(request.POST)
        if reset_password_token.check_token(user, request.resolver_match.kwargs.get("token")):
            password  = request.POST.get("password")
            password2 = request.POST.get("password2")
            if form.is_valid():
                user.set_password(str(password))
                user.save()
                messages.success(request, _("Success, Your password has been reset successfully"))
                return redirect(reverse("users:login"))
            else:
                display_form_validations(form=form, request=request)
        else:
            messages.error(request, _("Error, Invalid Link, please try again"))
    return render(request, "registration/change_password.html", {'resmessage':resmessage, 'show_form': show_form})