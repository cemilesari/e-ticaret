# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models

from main.core.models import TimeStampedModel

from autoslug import AutoSlugField

class Category(TimeStampedModel):
	class Meta:
		verbose_name = _("Category")
		verbose_name_plural = _("Categories")
		ordering = ("-created",)
	name = models.CharField(_("Name"), max_length=155,)
	slug = AutoSlugField(populate_from='name', unique=True)

	def __str__(self):
		return self.name
	def get_dict(self):
		return dict(
			pk = self.pk,
            name= self.name,
			slug=self.slug,
		)