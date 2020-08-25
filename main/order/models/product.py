# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.http import Http404
from main.core.models import TimeStampedModel, Currency
from main.users.models import User
from .category import Category
from .company import Company
from .branch import Branch
from ckeditor_uploader.fields import RichTextUploadingField
from autoslug import AutoSlugField
from django.views.generic.base import View
from django.views.generic.detail import BaseDetailView, SingleObjectTemplateResponseMixin
from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin

from django.utils.safestring import mark_safe

class ProductTemplate(TimeStampedModel):
    class Meta:
        verbose_name = _("Product Template")
        verbose_name_plural = _("Product Templates")
        ordering = ("-created",)
    PUBLISHED  = "published"
    SOLDOUT = "soldout"
    PASSIVE = "passive"
    DRAFT   = "draft"
    STATUSES = (
        (PUBLISHED, _("Published")),
        (SOLDOUT, _("Soldout")),
        (PASSIVE, _("Passive")),
        (DRAFT, _("Draft")),
    )
    USD = "usd"
    EUR = "eur"
    TRY = "try"
    CURRENCIES = (
        ("USD" , _("United States Dollar (USD)")),
        ("EUR" , _("Euro (EUR)")),
        ("TRY" , _("Turkish Lira (TRY)")),
    )
    name     = models.CharField(_("Name"), max_length=255,)
    slug     = AutoSlugField(populate_from='name', unique=True)
    image    = models.ImageField(_("Product"),upload_to=settings.DEFAULT_PRODUCT_FOLDER, blank=True, default=settings.DEFAULT_PRODUCT_IMAGE)
    body     = models.TextField(_("Description"), blank=True)
    left     = models.PositiveIntegerField(_("Product Left"), default=0,)
    count    = models.PositiveIntegerField(_("Product Count"), default=5,)
    user     = models.ForeignKey(User, verbose_name=_("Publisher"), on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name=_("Category"), on_delete=models.SET_NULL, null=True)
    company  = models.ForeignKey(Company, verbose_name=_("Company"), on_delete=models.CASCADE)
    original_price = models.FloatField(_("Original Price"), default=10.0,)
    price    = models.FloatField(_("Price"), default=5.0,)
    currency = models.CharField("Currency",  max_length=100, choices=CURRENCIES,default=TRY,)
    status   = models.CharField(_("Status"), max_length=55, choices=STATUSES, default=DRAFT,)
    is_deleted = models.BooleanField(_("Is Deleted"), default=False)

    def __str__(self):
        return self.name
    def get_template(self):
        return name_set.all()
    def get_dict(self):
        return dict(
            pk= self.pk,
            name  = self.name,
            slug  = self.slug,
            image = self.image,
            body  = self.body,
            left  = self.left,
            count = self.count, 
            user  =self.user.get_dict() if self.user else {}, 
            category  =self.category.get_dict() if self.category  else {},
            company   =self.company.get_dict() if self.company else {},
            original_price  =self.original_price,
            price     =self.price,
            currency  =self.currency.get_dict() if self.currency else  {},
            status    =self.status,
            is_deleted =self.is_deleted,
        )

class Product(TimeStampedModel):
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ("-created",)
    ACTIVE = "active"
    DRAFT = "draft"
    STATUSES = (
        (ACTIVE, _("Active"),),
        (DRAFT, _("Draft"),),
    )
    branch    = models.ForeignKey(Branch, verbose_name=_("Branch"), on_delete=models.CASCADE)
    template  = models.ForeignKey(ProductTemplate, verbose_name=_("Product Template"), on_delete=models.SET_NULL, null=True)
    left      = models.PositiveIntegerField(_("Product Left"), default=0,)
    detail    = RichTextUploadingField(blank=True,null=True)
    count     = models.PositiveIntegerField(_("Product Count"), default=5,)
    user  = models.ForeignKey(User, verbose_name=_("Publisher"), on_delete=models.CASCADE)
    original_price = models.FloatField(_("Original Price"), default=10.0,)
    price     = models.FloatField(_("Price"), default=5.0,)
    start_time = models.TimeField(_("Start Time"))
    end_time   = models.TimeField(_("End Time"))
    sold_time  = models.TimeField(_("Sold Time"))
    status = models.CharField(_("Status"), max_length=55, choices=STATUSES, default=DRAFT,)
    is_deleted = models.BooleanField(_("Is Deleted"), default=False)
    image = models.ImageField(_("Product Image"), upload_to=settings.DEFAULT_PRODUCT_FOLDER, blank=True, default=settings.DEFAULT_PRODUCT_IMAGE)
    def __str__(self):
        return self.template.name if self.template else _("Untitled")
        
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def get_dict(self):
        return dict(
            pk=self.pk,
            branch    =self.branch.get_dict() if self.branch else {}  , 
            template  =self.template.get_dict() if self.template else {}, 
            left      =self.left    , 
            count     =self.count   , 
            user      =self.user.get_dict()  if self.user else {}   , 
            original_price = self.original_price, 
            price      = self.price,      
            currency   = self.currency.get_dict() if self.curreny else {}, 
            start_time =self.start_time,
            end_time   =self.end_time,
            sold_time  =self.sold_time, 
            status     = self.status,     
            is_deleted =self.is_deleted,
            image      =self.image, 
        )


class YearMixin:
    year_format = '%Y'
    year = None
    def get_year(self):
        year = self.year
        if year is None:
            try:
                year = self.kwargs['year']
            except KeyError:
                try: 
                    year = self.request.GET['year']
                except KeyError:
                    raise Http404(_('No year specified'))
        return year 

class Images(TimeStampedModel):
    product = models.ForeignKey(Product, verbose_name=_("Product For Image"), on_delete=models.CASCADE)
    title = models.CharField(_("Image Title"),max_length=50, blank=True)
    image = models.ImageField(_("Product Image"), upload_to=settings.DEFAULT_PRODUCT_FOLDER, blank=True, default=settings.DEFAULT_PRODUCT_IMAGE)
    def __str__(self):
        return self.title
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'
