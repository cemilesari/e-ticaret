# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils import timezone as djtz
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.urls import reverse
from main.users.models import User
from main.core.tasks import mail_html_maillist
from main.core.tokens import *
from main.core.models import Tokenizer

import logging
logger = logging.getLogger(__name__)
def account_activation(user=None):
    ret = None
    try:
        uidb64      = urlsafe_base64_encode(force_bytes(user.pk))
        tokinzer    = EmailActiveTokenGenerator()
        token       = tokinzer.make_token(user)
        ob,sv = Tokenizer.objects.get_or_create(uidb64=uidb64,token=token)
        subject     = str(_("Activate Your account"))
        template_name   = "emails/auth/account_activation.html"
        title = str(_("Please verfiy your email to activate account"))
        if token:
            print(token)
            print("token var")
            current_site = "{0}{1}".format(settings.HOST_SCHEMA, settings.DOMAIN_NAME,).strip("/")
            dev_url = reverse('users:email_verification', kwargs={'uidb64': uidb64, 'token':token})
            confirm_url = "{}{}".format(current_site,dev_url)
            if settings.DEBUG:
                print('confirm_url: ', confirm_url)
            c = dict(    
                #user=user,
                title_message=title,
                site_url=current_site,
                confirm_url=confirm_url,
                current_site=current_site,
            )

            mail_html_maillist.apply_async(args=([user.email], subject, template_name, c, settings.LANGUAGE_CODE,))
            ret = True
    except Exception as e:
        print("token yok")
        logger.error("{} account active email ".format(e))
    return ret


def account_rest(user=None):
    ret = None
    try: 
        uidb64         = urlsafe_base64_encode(force_bytes(user.pk))
        tokinzer       = RestPasswordTokenGenerator()
        token          = tokinzer.make_token(user)
        ob, sv         = Tokenizer.objects.get_or_create(uidb64=uidb64, token=token)
        subject        = str(_("Rest Password"))
        template_name  = "emails/auth/rest.html"
        title          = str(_("You recently requested to reset your account password."))
        if token : 
            current_site = "{0}{1}".format(settings.HOST_SCHEMA, settings.DOMAIN_NAME,).strip("/")
            dev_url      = reverse('users:password_rest_verification', kwargs= {'uidb64':uidb64, 'token':token})
            confirm_url  = "{}{}".format(current_site, dev_url)
            if settings.DEBUG:
                print('confirm_url:', confirm_url)
            c = dict(
                title_message=title,
                site_url=current_site,
                confirm_url=confirm_url,
                current_site=current_site,
            )
            mail_html_maillist.apply_async(args=([user.email], subject, template_name, c, settings.LANGUAGE_CODE,))
            ret = True
    except Exception as e:
        logger.error("{} account active email".format(e))
    return ret 

def password_changed(user):
    ret = None
    try:
        subject       = str(_("Your Password Has Been Changed"))
        template_name = "emails/notify/password._changed.html"
        title         = str(_("Your account password recently changed"))
        current_site  = "{0}{1}".format(settings.HOST_SCHEMA, settings.DOMAIN_NAME,).strip("/")
        c = dict(
            title_message = title, 
            site_url = current_site,
            confirm_url = confirm_url,
            current_site = current_site,
        )
        mail_html_maillist.apply_async(args=([user.email], subject, template_name, c, settings.LANGUAGE_CODE,))
        ret = True
    except Exception as e:
        logger.error("{} account active mail".format(e))
    return ret 

