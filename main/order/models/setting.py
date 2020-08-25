# -*- encoding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models

from main.core.models import TimeStampedModel, Currency
from django.conf import settings



class Setting(TimeStampedModel):
    verbose_name = _("Setting")
    verbose_name_plural = _("Settings")
    ordering = ("-created",)
    TRUE = "true"
    FALSE = "false"
    STATUS = (
        (TRUE, _("True"),),
        (FALSE, _("False"),),
    )
    status       = models.CharField(_("Status"),max_length=10, choices=STATUS)
    title        = models.CharField(_("Title"),max_length=150, blank=True)
    keywords     = models.CharField(_("Keywords"),max_length=150, blank=True)
    description  = models.CharField(_("Description"),max_length=255, blank=True)
    company      = models.CharField(_("Company"),max_length=150, blank=True)
    address      = models.CharField(_("Address"),max_length=150, blank=True)
    phone        = models.CharField(_("Phone"),max_length=150, blank=True)
    fax          = models.CharField(_("Fax"),max_length=150, blank=True)
    email        = models.CharField(_("Email"),max_length=150, blank=True)
    smtpserver   = models.CharField(_("Smtp Server"),max_length=150, blank=True)
    smtpemail    = models.CharField(_("Smtp Email"),max_length=150, blank=True)
    smtppassword = models.CharField(_("Smtp Password"),max_length=150, blank=True)
    smtpport     = models.CharField(_("Smtp Port"),max_length=150, blank=True)
    icon         = models.ImageField(_("Icon"), upload_to=settings.DEFAULT_PRODUCT_FOLDER, blank=True, default=settings.DEFAULT_PRODUCT_IMAGE)
    facebook     = models.CharField(_("Facebook"),max_length=50, blank=True)
    instagram    = models.CharField(_("Instagram"),max_length=50, blank=True)
    twitter      = models.CharField(_("Twitter"),max_length=50, blank=True)
    aboutus      = models.TextField(blank=True,null=True)
    contactus      = models.TextField(blank=True,null=True)
    references   = models.TextField(blank=True,null=True)
    def __str__(self):
        return title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.icon.url))
    image_tag.short_description = 'Image'
