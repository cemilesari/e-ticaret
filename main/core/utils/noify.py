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


def send_email_activeation(user_id):
    user = None
    ret = False
    try:
        user    = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        LogThat(msg="send_email_activeation error User not found user_id {}".format(user_id))
    try:
        uidb64  = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        token   = email_active_token.make_token(user)
        subject = str(_("Activate Your Account"))
        template_name   = "core/email_active.html"
        if token:
            current_site = "{0}{1}".format(settings.HOST_SCHEMA, settings.DOMAIN_NAME,).strip("/")
            email_confirm_url = "{}{}".format(current_site,reverse('email_verification', kwargs=dict(uidb64=uidb64,token=token,)))
            c = dict(
                email=user.email,
                welcome_message=_("Activate Your Account"),
                site_url=current_site,
                email_confirm_link=email_confirm_url,
                current_site=current_site,
                WHITE_LOGO_EMAIL=settings.WHITE_LOGO,
            )
            mail_html_maillist.apply(args=([user.email], subject, template_name, c, settings.LANGUAGE_CODE,))
            ret = True
    except Exception as e:
        print(e)
        LogThat(msg="send_email_activeation error {}".format(e))
    return ret

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
            reset_password_confirm = "{}{}".format(current_site,reverse('change_password_from_email', kwargs=dict(uidb64=uidb64,token=token,)))
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

def new_payment_email(payment_id):
    ret = None
    try:
        from main.subscription.models import Payment
        payment_obj = Payment.objects.get(pk=int(payment_id))
    except Payment.DoesNotExist:
        LogThat(msg="new_payment_email error Payment not found payment_id {}".format(payment_id))
        ret = False
    try:
        if payment_obj is not None:
            current_site = "{0}{1}".format(settings.HOST_SCHEMA, settings.DOMAIN_NAME,).strip("/")
            payment_link = "{}{}".format(current_site, reverse('subscription:payment_guid', kwargs=dict(guid=payment_obj.guid)))
            site_name = settings.SITE_NAME
            c = dict(
                email=payment_obj.user.email,
                welcome_message=_("New Invoice %(payment_id)s") % dict(payment_id=payment_obj.payment_id),
                site_url=current_site,
                site_name=site_name,
                paylink=payment_link,
                current_site=current_site,
                WHITE_LOGO_EMAIL=settings.WHITE_LOGO,
            )
            subject         = str(_("%(site_name)s New Invoice") % dict(site_name=site_name))
            template_name   = "core/subscription/new_payment.html"
            mail_html_maillist.apply(args=([payment_obj.user.email], subject, template_name, c, settings.LANGUAGE_CODE,))
            ret = True
    except Exception as e:
        LogThat(msg="new_payment_email error {}".format(e))
        ret = False
    return ret

def new_subscription_email(subscription_id=None,free=None):
    ret = None
    try:
        from main.subscription.models import Subscription
        subscription_obj = Subscription.objects.get(pk=int(subscription_id))
    except Subscription.DoesNotExist:
        LogThat(msg="new_payment_email error Subscription not found subscription_id {}".format(subscription_id))
        ret = False
    try:
        if subscription_obj is not None:
            current_site = "{0}{1}".format(settings.HOST_SCHEMA, settings.DOMAIN_NAME,).strip("/")
            site_name = settings.SITE_NAME
            if free:
                welcome_messagemsg = _("Your Trial Subscription %(subscription_id)s") % dict(subscription_id=subscription_obj.name)
            else:
                welcome_messagemsg = _("New Subscription %(subscription_id)s") % dict(subscription_id=subscription_obj.name)
            c = dict(
                email=subscription_obj.user.email,
                welcome_message=welcome_messagemsg,
                site_url=current_site,
                freesub=free,
                site_name=site_name,
                subscription=subscription_obj,
                current_site=current_site,
                WHITE_LOGO_EMAIL=settings.WHITE_LOGO,
            )
            subject         = str(_("%(site_name)s New Subscription") % dict(site_name=site_name))
            template_name   = "core/subscription/new_subscription.html"
            mail_html_maillist.apply(args=([subscription_obj.user.email], subject, template_name, c, settings.LANGUAGE_CODE,))
            ret = True
    except Exception as e:
        LogThat(msg="new_subscription_email error {}".format(e))
        ret = False
    return ret

def status_email(booking_id):
    ret = None
    try:
        from main.subscription.models import Booking
        booking_obj = Booking.objects.get(pk=int(booking_id))
    except Booking.DoesNotExist:
        LogThat(msg="status_email error Booking not found booking_id {}".format(booking_id))
        ret = False
    try:
        if booking_obj is not None:
            current_site = "{0}{1}".format(settings.HOST_SCHEMA, settings.DOMAIN_NAME,).strip("/")
            site_name = settings.SITE_NAME
            c = dict(
                email=booking_obj.student.email,
                welcome_message=_("Booking Status %(booking_id)s") % dict(booking_id=booking_obj.booking_id),
                site_url=current_site,
                site_name=site_name,
                booking=booking_obj,
                current_site=current_site,
                WHITE_LOGO_EMAIL=settings.WHITE_LOGO,
            )
            subject         = str(_("%(site_name)s Booking Status") % dict(site_name=site_name))
            template_name   = "core/subscription/status.html"
            mail_html_maillist.apply(args=([booking_obj.student.email], subject, template_name, c, settings.LANGUAGE_CODE,))
            ret = True
    except Exception as e:
        LogThat(msg="status_email error {}".format(e))
        ret = False
    return ret