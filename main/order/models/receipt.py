# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models

from main.core.models import TimeStampedModel, Currency
from main.users.models import User
from .product import Product

from autoslug import AutoSlugField

class Receipt(TimeStampedModel):
    class Meta:
        verbose_name = _("Receipt")
        verbose_name_plural = _("Receipts")
        ordering = ("-created",)
    user     = models.ForeignKey(User, verbose_name=_("Consumer"), on_delete=models.SET_NULL, null=True)
    product  = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.SET_NULL, null=True)
    count    = models.PositiveIntegerField(_("Item Count"), default=1, help_text=_("Number of product item that consumer bought"))
    original_price = models.FloatField(_("Original Price"), default=10.0,)
    price    = models.FloatField(_("Price"), default=5.0,)
    total_price = models.FloatField(_("Price"), default=5.0, help_text=_("Total Price that paid, it is represet price x count = total"))
    currency = models.ForeignKey(Currency, verbose_name=_("Currency"), on_delete=models.SET_NULL, null=True)
    payment_id = models.CharField(_("Payment ID"), max_length=155, null=True, blank=True,)
    holder   = models.CharField(_("Card Holder Name"), max_length=120, null=True, blank=True)
    has_paid  = models.BooleanField(_("Has Paid"), default=False)

    def __str__(self):
        return "%(full_name)s %(product)s" % dict(full_name=self.user, product=self.product)
    def get_dict(self):
        return dict(
            pk=self.pk,
            user     =self.user.get_dict()  if self.user else {},    
            product  =self.product.get_dict() if self.product else {},
            count    =self.count,
            original_price =self.original_price,
            price    =  self.price,
            total_price    = self.total_price,
            currency = self.currency.gey_dict() if self.currency else {},
            payment_id     = self.payment_id,
            holder   = self.holder,
            has_paid =self.has_paid,
        )