# -*- encoding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from main.core.utils import USER_SEARCH_FIELDS
from ..models import Favorite

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
	list_display = ("user", "product", "rate", "created")
	list_filter = ("rate",)
	#search_fields = ("product__name",) + USER_SEARCH_FIELDS
	date_hierarchy = "created"