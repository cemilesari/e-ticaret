# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.exceptions import ValidationError

from main.core.models import TimeStampedModel
from main.users.models import User

class Ticket(TimeStampedModel):
    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")

    OPEN = "open"
    CLOSED = "closed"
    SUPPORT = "support"
    OTHER = "other"
    HIGH = "high"
    LOW = "low"

    STATUSES = (
    	(OPEN, _("Open"),),
    	(CLOSED, _("Closed"),),
    )

    TYPES = (
    	(SUPPORT, _("Support"),),
    	(OTHER, _("Other"),),
    )

    PRIORITIES = (
    	(HIGH, _("High"),),
    	(LOW, _("Low"),),
    )

    user            = models.ForeignKey(User, blank=True, null=True , on_delete=models.SET_NULL)

    ticket_name     = models.CharField(verbose_name=_("Ticket Name"), max_length=200, blank=True)
    ticket_subject  = models.CharField(verbose_name=_("Ticket Subject"), max_length=200, blank=True)
    ticket_status   = models.CharField(_("Ticket Status "), max_length=32, default=OPEN, choices=STATUSES)
    ticket_type     = models.CharField(_("Ticket Type "), max_length=32, default=OTHER, choices=TYPES)
    ticket_priority = models.CharField(_("Ticket Priority"), max_length=32, default=LOW, choices=PRIORITIES)
    ticket_desc     = models.TextField(_("Ticket Description"),blank=True, null=True , default='')


    def new_message(self,message="",user=None):
        obj = TicketMessage(
            user=user,
            ticket=self,
            message=message,
        )
        obj.save()
        return obj

    def is_opened_ticket(self):
        return True if self.ticket_status == Ticket.OPEN else False

    def get_messages(self):
        return TicketMessage.objects.filter(ticket=self).order_by('created')

    def get_last_update_(self):
        return TicketMessage.objects.filter(ticket=self).latest('created').created

    def __str__(self):
        return str(self.ticket_name)

class TicketMessage(TimeStampedModel):
    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    user            = models.ForeignKey(User, blank=True, null=True , on_delete=models.SET_NULL)
    ticket          = models.ForeignKey(Ticket, blank=True, null=True , on_delete=models.SET_NULL)
    message         = models.TextField(_("Message"),blank=True, null=True, default='')

    def clean(self):
        if self.ticket.ticket_type == Ticket.CLOSED:
            raise ValidationError('Ticket Already Closed !')

        if self.user == self.ticket.user:
            pass
        else:
            raise ValidationError('Not same Ticket User !')

    def __str__(self):
        return "Ticket {}".format(self.id)
