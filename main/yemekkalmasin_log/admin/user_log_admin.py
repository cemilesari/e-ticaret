import json
from datetime import date, timedelta
from functools import update_wrapper

from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from main.yemekkalmasin_log.models import UserLog


class UserLogAdmin(admin.ModelAdmin):
    list_display = ('log_name', 'user', 'internel_name',)
  

admin.site.register(UserLog, UserLogAdmin)