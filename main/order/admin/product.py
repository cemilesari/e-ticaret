# -*- encoding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from main.core.utils import USER_SEARCH_FIELDS
from ..models import Product, ProductTemplate,Images



class ProductImageInline(admin.TabularInline):
	model = Images
	extra = 5

@admin.register(ProductTemplate)
class ProductTemplateAdmin(admin.ModelAdmin):
	list_display = ("name", "left", "count", "user", "category", "company", "original_price", "price", "currency", "status", "is_deleted",)
	list_filter = ("category", "status", "is_deleted", "currency",)
	search_fields = ("name", "category__name", "company__name",) + USER_SEARCH_FIELDS
	date_heirarchy = "created"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ("branch", "template", "left", "count", "user", "original_price", "price", "start_time", "end_time", "sold_time", "status", "is_deleted",'image_tag',)
	list_filter = ("status", "is_deleted", )
	readonly_fields = ('image_tag',)
	search_fields = ("branch__name", "template__name",) + USER_SEARCH_FIELDS
	date_heirarchy = "created"
	inlines = [ProductImageInline]


@admin.register(Images)
class ProductImageAdmin(admin.ModelAdmin):
	list_display = ("product", "title" ,"image_tag")
	list_filter = ("product", )
	readonly_fields = ('image_tag',)
	date_heirarchy = "created"
