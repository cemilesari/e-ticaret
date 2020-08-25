from __future__ import unicode_literals, absolute_import
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from main.users.models import User

from ..models import Ticket, TicketMessage

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
	list_display = ("user","ticket_name", "ticket_subject", "ticket_status", "ticket_type","ticket_priority","ticket_desc",)
	search_fields = ("user", "ticket_subject", "ticket_status", "ticket_type", "ticket_priority",)

@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
	list_display = ("message","ticket_id" )