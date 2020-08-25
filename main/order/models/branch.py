# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models

from main.core.models import TimeStampedModel
from main.users.models import User
from .location import Location
from .company import Company

from autoslug import AutoSlugField

class Branch(TimeStampedModel):
	class Meta:
		verbose_name = _("Branch")
		verbose_name_plural = _("Branches")
		ordering = ("-created",)
	name = models.CharField(_("Name"), max_length=155,)
	slug = AutoSlugField(populate_from='name', unique=True)
	body = models.TextField(_("About Branch"), blank=True)
	user = models.ForeignKey(User, verbose_name=_("Manager"), on_delete=models.SET_NULL, null=True)
	location = models.ForeignKey(Location, verbose_name=_("Location"), on_delete=models.SET_NULL, null=True)
	company  = models.ForeignKey(Company, verbose_name=_("Company"), on_delete=models.CASCADE,)
	is_deleted = models.BooleanField(_("Is Deleted") , default=False)
	def __str__(self):
		return self.name
	def get_dict(self):
		return dict(
			pk=self.pk,
			name=self.name,
			slug= self.slug,
			body=self.body,
			user=self.user,
			location=self.location,
			company= self.company.get_dict() if self.company else {} ,
		)