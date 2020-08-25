
# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils import timezone as djtz
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.urls import reverse
from main.core.logger import LogThat
from main.users.models import User
from main.core.tasks import mail_html_maillist
from main.core.tokens import *

def send_password_rest_email(user_id):
    ret = None
    try: 
        user = User.objects.get(pk=int(user_id))
    except User.DoesNotExist:
        LogThat(msg="send_password_rest_email error User not found user_id {}".format(user_id))
        ret = False
    try:
        if user is not None:
            current_site = "{0}{1}".format(settings.HOST_SCHEMA, settings.DOMAIN_NAME,).strip("/")
            uidb64  = urlsafe_base64_encode(force_bytes(user.pk)).decode()
            token   = reset_password_token.make_token(user)
            reset_password_confirm = "{}{}".format(current_site,reverse('users:change_password_from_email', kwargs=dict(uidb64=uidb64,token=token,)))
            site_name = settings.SITE_NAME
            c = dict(
                email=user.email,
                welcome_message=_("Reset Your password on %(site_name)s") % dict(site_name=site_name),
                site_url=current_site,
                site_name=site_name,
                reset_password_confirm=reset_password_confirm,
                current_site=current_site,
                WHITE_LOGO_EMAIL=settings.WHITE_LOGO,
            )
            subject         = str(_("%(site_name)s Reset Password") % dict(site_name=site_name))
            template_name   = "core/reset/password_reset_email.html"
            mail_html_maillist.apply(args=([user.email], subject, template_name, c, settings.LANGUAGE_CODE,))
            ret = True
    except Exception as e:
        LogThat(msg="send_password_rest_email error {}".format(e))
        ret = False
    return ret
