# -*- encoding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from ..models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("name",)
	search_fields = ("name",)