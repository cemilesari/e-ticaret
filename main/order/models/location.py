# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models

from main.core.models import TimeStampedModel

from autoslug import AutoSlugField
from main.users.models import User

class Location(TimeStampedModel):
    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        ordering = ("-created",)
    user = models.ForeignKey(User, verbose_name=_("Owner"), on_delete=models.SET_NULL, null=True)
    address = models.CharField(verbose_name=_("Address"), max_length=55)
    city    = models.CharField(verbose_name=_("City"), max_length=55)
    state   = models.CharField(verbose_name=_("State"), max_length=55)
    country = models.CharField(verbose_name=_("Country"), max_length=55)
    zipcode = models.CharField(verbose_name=_("Zipcode"), max_length=55)
    lati    = models.FloatField(_("Latitude"), default=0.0)
    lngt    = models.FloatField(_("Longitude"), default=0.0)
    mob     = models.CharField(_("Mobile"), max_length=15)
    tel     = models.CharField(_("Telephone"), max_length=15)
    fax     = models.CharField(_("Fax"), max_length=15)
    url     = models.CharField(_("Website"), max_length=155)
    mail    = models.CharField(_("Mail"), max_length=155)
    tax_id     = models.CharField(_("TAX ID"), max_length=25)
    tax_branch = models.CharField(_("TAX Branch"), max_length=25)
    is_deleted = models.BooleanField(_("Is Deleted"), default=False)

    def __str__(self):
        return self.address
    def get_dict(self): 
        return dict(
            pk = self.pk,
            address = self.address,
            city    = self.city,
            state   = self.state,
            country = self.country,
            zipcode = self.zipcode,
            lati    = self.lati,
            lngt    = self.lngt,
            mob     = self.mob,
            tel     = self.tel,
            fax     = self.fax,
            url     = self.url,
            mail    = self.mail,
            tax_id  = self.tax_id, 
            tax_branch = self.tax_branch,
        )