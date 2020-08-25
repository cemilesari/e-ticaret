from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import View
from django.contrib.auth import login
from django.http import Http404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.shortcuts import get_object_or_404

from rest_framework_jwt.compat import get_username, get_username_field
from rest_framework_jwt.settings import api_settings

from main.users.models import User
from main.core.utils.security import check_two_factor_authentication
from main.core.utils.cryptograph import sha1
from main.core.tokens import *
from main.core.models import Tokenizer
from main.yemekkalmasin_log.utils import user_event

import uuid,warnings
from calendar import timegm
from datetime import datetime
import time
import random

jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

def session_payload(user,auth_2fa=False):
    username_field = get_username_field()
    username = get_username(user)

    warnings.warn(
        'The following fields will be removed in the future: '
        '`email` and `user_id`. ',
        DeprecationWarning
    )

    payload = {
        'user_id': user.pk,
        'username': sha1(username),
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }

    if hasattr(user, 'email'):
        payload['email'] = user.email
    if isinstance(user.pk, uuid.UUID):
        payload['user_id'] = sha1(str(user.pk))

    payload[username_field] = username

    payload['tfa_enabled'] = user.get_user_security_setting().two_factor_authentication_enabled
    payload['tfa'] = auth_2fa

    if auth_2fa:
        payload['tfa_time_stamp'] = time.time()
    else:
        payload['tfa_time_stamp'] = None

    for i in range(1,3):
        payload[random.randint(3,10)] = sha1(random.randint(20,32))

    return jwt_encode_handler(payload)


class TwoFactor(View):
    template_name = 'auth/twofactor.html'
    
    def get(self, request, *args, **kwargs):
        data = None
        is_sso = True if str(request.resolver_match.kwargs.get('sso')) == 'sso' else False
        try:
            data = jwt_decode_handler(request.session[settings.SESSION_ID_KEY])
        except:
            pass
        if not data:
            return redirect('/')

        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        otp_code = request.POST.get("code", 0)
        _sso = request.POST.get("sso", 0)
        is_sso = True if str(_sso) == 'sso' else False
        print('is_sso: ', is_sso)

        data, user_obj = None, None
        
        try:
            data = jwt_decode_handler(request.session[settings.SESSION_ID_KEY])
        except:
            pass
        
        if not data:
            return redirect('/')
        try:
            user_obj = User.objects.get(pk=int(data['user_id']), username=str(data['username']) , email=str(data['email']))
        except:
            pass

        if not user_obj:
            return redirect('/')

        sec_key = user_obj.get_user_security_setting().two_factor_authentication_key
        otp_check = check_two_factor_authentication(sec_key,otp_code)
        if otp_check:
            sessionkey = session_payload(user_obj,auth_2fa=True)
            print('sessionkey: ', sessionkey)
            request.session[settings.SESSION_ID_KEY] = sessionkey
            user_event(log_name="OTP success",log_text="User OTP Code has been verified",user=user_obj)
            login(request,user_obj)
            if is_sso:
                print('hh')
                return redirect(settings.PRO_TRADING_LOGIN_URL+request.session[settings.SESSION_ID_KEY])
            else:
                return redirect('/')
        else:
            messages.error(request, _('OTP Error, Invalid OTP Code, please try again'))

        return render(request, self.template_name, {})

class DeviceVerification(View):
    template_name = 'auth/device_verification.html'

    def get(self, request, *args, **kwargs):
        required_fields = ["uidb64", "token"]
        msg = None
        if all(param in request.resolver_match.kwargs for param in required_fields):
            uid         = force_text(urlsafe_base64_decode(request.resolver_match.kwargs.get("uidb64")))
            user        = get_object_or_404(User, pk=uid)
            tokinzer_db = get_object_or_404(Tokenizer, uidb64=urlsafe_base64_encode(force_bytes(user.pk)), token=request.resolver_match.kwargs.get("token"))
            if tokinzer_db.expired_or_operated():
                raise Http404("404")
            tokinzer    = DeviceTokenGenerator()
            token_check = tokinzer.check_token(user, request.resolver_match.kwargs.get("token"))
            if user and token_check:
                user.is_device_locked = False
                user.save()
                tokinzer_db.delete()
                user_event(log_name="New verified Device",log_text="new device has been successfully added",user=user)

                msg = _("Your Device has been verified successfully")
        else:
            raise Http404
        return render(request, self.template_name, {'msg':msg})


class EmailVerification(View):
    template_name = 'auth/email_verification.html'

    def get(self, request, *args, **kwargs):
        required_fields = ["uidb64", "token"]
        msg = None
        if all(param in request.resolver_match.kwargs for param in required_fields):
            uid         = force_text(urlsafe_base64_decode(request.resolver_match.kwargs.get("uidb64")))
            user        = get_object_or_404(User, pk=uid)
            tokinzer_db = get_object_or_404(Tokenizer, operated=False, uidb64=urlsafe_base64_encode(force_bytes(user.pk)), token=request.resolver_match.kwargs.get("token"))
            if tokinzer_db.expired_or_operated():
                raise Http404
            tokinzer    = EmailActiveTokenGenerator()
            token_check = tokinzer.check_token(user, request.resolver_match.kwargs.get("token"))
            if user and token_check:
                user.is_active = True
                user.email_verified = True
                user.save()
                tokinzer_db.operated = True
                tokinzer_db.save()
                user_init_wallets.apply_async([{'user':user.pk}])
                user_event(log_name="User Email verified",log_text="user email has been verified",user=user)
                msg = _("Your Email has been verified successfully")
        else:
            raise Http404
        return render(request, self.template_name, {'msg':msg})