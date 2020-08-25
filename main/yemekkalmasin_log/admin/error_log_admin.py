from __future__ import unicode_literals
import logging 
from django.conf import settings 
from django.contrib import admin
from django.utils.html import format_html 
from main.yemekkalmasin_log.models import ErrorLog, RequestLog

class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ('colored_msg', 'traceback', 'create_datetime_format')
    list_display_links = ('colored_msg', )
    list_filter = ('level', )
    list_per_page = getattr(settings, 'DJANGO_DB_LOGGER_ADMIN_LIST_PER_PAGE', 10)

    def colored_msg(self, instance):
        if instance.level in [logging.NOTSET, logging.INFO]:
            color = 'green'
        elif instance.level in [logging.WARNING, logging.DEBUG]:
            color = 'orange'
        else:
            color = 'red'
        return format_html('<span style="color: {color};">{msg}</span>', color=color, msg=instance.msg)

    colored_msg.short_description = 'Error Message'

    def traceback(self, instance):
        return format_html('<pre><code>{content}</code></pre>', content=instance.trace if instance.trace else '')

    def create_datetime_format(self, instance):
        return instance.created.strftime('%Y-%m-%d %X')
    create_datetime_format.short_description = 'Created at'

admin.site.register(ErrorLog, ErrorLogAdmin)