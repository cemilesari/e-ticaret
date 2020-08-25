# -*- encoding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from main.core.utils import USER_SEARCH_FIELDS

from ..models import Branch

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
	list_display = ("name", "user", "location", "company",)
	list_filter = ("company",)
	search_field = ("company__name",) + USER_SEARCH_FIELDS