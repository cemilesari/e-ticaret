# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models

from main.core.models import TimeStampedModel
from main.users.models import User
from .product import Product

from autoslug import AutoSlugField

class Favorite(TimeStampedModel):
	class Meta:
		verbose_name = _("Favorite")
		verbose_name_plural = _("Favorites")
		ordering = ("-created",)
	user    = models.ForeignKey(User, verbose_name=_("Consumer"), on_delete=models.CASCADE)
	product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE)
	rate    = models.PositiveIntegerField(_("Rate"),)
	body    = models.TextField(_("Message"),)
	
	
	def __str__(self):
		return str(self.product.template.name)
	
	def get_dict(self):
		basedict = super(Favorite, self).get_dict().copy()
		return dict(
			user=self.user.get_dict() if self.user else {},
			product=self.product.get_dict() if self.product else {},
			rate=self.rate,
			body=self.body,
			**basedict,
		)