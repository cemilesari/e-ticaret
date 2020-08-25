# -*- encoding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from main.core.utils import USER_SEARCH_FIELDS
from ..models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
	list_display = ("name", "user", "size", "category", "location", "created",'is_deleted',)
	list_filter = ("size", "category",)
	search_fields = ("name",) + USER_SEARCH_FIELDS
	date_hierarchy = "created"