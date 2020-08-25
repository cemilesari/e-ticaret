# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from main.core.models import TimeStampedModel
from main.users.models import User
from .location import Location

from autoslug import AutoSlugField
from django.utils.text import slugify
import os, re


def _handle_site_logo(instance, filename):
    site_name = slugify(instance.name)
    name, extension = os.path.splitext(filename)
    combine_name = "{}_{}".format(site_name, slugify(name))

    new_filename = "{0}{1}".format(combine_name, extension)
    return "{}/{}".format("site-logos", new_filename)


class Company(TimeStampedModel):
    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
        ordering = ("-created",)
    RESTAURANT  = "restaurant"
    HOTEL       = "hotel"
    SUPERMARKET = "supermarket"
    BAKERY      = "bakery"
    GREENGROCER = "greengrocer"
    SPECIALITY  = "speciality"
    CATEGORIES = (
        (RESTAURANT, _("Restaurant"),),
        (HOTEL, _("Hotel"),),
        (SUPERMARKET, _("Supermarket"),),
        (BAKERY, _("Bakery"),),
        (GREENGROCER, _("Greengrocer"),),
        (SPECIALITY, _("Speciality"),),
    )
    SMALL  = "small"
    MIDDLE = "middle"
    LARGE  = "large"
    BIG    = "big"
    SIZES = (
        (SMALL, _("Small 0-10"),),
        (MIDDLE, _("Middle 10-50"),),
        (LARGE, _("Large 50-200"),),
        (BIG, _("Big 200-more"),),
    )
    name = models.CharField(_("Name"), max_length=155)
    slug = AutoSlugField(populate_from='name', unique=True)
    body = models.TextField(_("About Company"), blank=True)
    logo = models.ImageField(_("Logo"), upload_to=_handle_site_logo, blank=True, default=settings.DEFAULT_COMPANY_LOGO)
    user = models.ForeignKey(User, verbose_name=_("Owner"), on_delete=models.SET_NULL, null=True)
    size = models.CharField(_("Company Size"), choices=SIZES, default=SMALL, max_length=55)
    category = models.CharField(_("Category"), choices=CATEGORIES, default=RESTAURANT, max_length=55)
    location = models.ForeignKey(Location, verbose_name=_("Location"), on_delete=models.SET_NULL, null=True)
    is_deleted = models.BooleanField(_("Is Deleted"), default=False)
    def __str__(self):
        return str(self.name)
    def branches(self):
        return self.branch_set.distinct()
    def get_dict(self):
        return dict(
            pk   = self.pk,
            name = self.name, 
            slug = self.slug,
            body = self.body,
            logo = self.logo,
            user = self.user.get_dict() if self.user else {},
            size = self.size,
            category = self.category,
            location = self.location.get_dict() if self.location else {},     
        )
    def save(self, *args, **kwargs):
        if not self.id: # CREATED
            pass
        else: # UPDATED
            pass
        super(Company, self).save(*args, **kwargs)
    