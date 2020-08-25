# -*- encoding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from ..models import Location

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
	list_display = ("user","address", "city", "state", "country", "zipcode", "lati", "lngt", "mob", "tel", "fax", "url", "mail", "tax_id", "tax_branch","is_deleted", )
	search_fields = list_display
	date_hierarchy = "created"