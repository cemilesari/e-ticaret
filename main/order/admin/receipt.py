# -*- encoding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from main.core.utils import USER_SEARCH_FIELDS
from ..models import Receipt

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
	list_display = ("user", "product", "count", "original_price", "price", "total_price", "currency", "payment_id", "holder", "has_paid",)
	list_filter = ("currency", "has_paid",)
	search_fields = ("product__name", "original_price", "price", "total_price", "payment_id", "holder",) + USER_SEARCH_FIELDS