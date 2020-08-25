# -*- encoding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from main.core.utils import USER_SEARCH_FIELDS
from ..models import Setting

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
	list_display = ("status", "title","description", "facebook", "twitter", "instagram", "email", "smtpserver", "image_tag", "smtpemail", "smtppassword",)
	list_filter = ("status", "title",)
