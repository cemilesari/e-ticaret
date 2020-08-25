from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.views import View
from main.core.utils import get_query
from django.utils import timezone as djtz

from main.core.utils import paginate,str2date
from main.yemekkalmasin_log.utils import user_event
from main.core.utils import generate_ticket_name
from main.tickets.models import Ticket, TicketMessage
from main.tickets.forms import NewTicketForm,NewTicketForm
from main.core.utils import display_form_validations


class TicketView(View):
    template_name = 'ticket/tickets_list.html'

    ctx = {}

    def get(self, request, *args, **kwargs):
        tickets = Ticket.objects.filter(user=request.user)
        title           = request.GET.get("title",None)
        ticket_type     = request.GET.get("ticket_type",None)
        ticket_status   = request.GET.get("ticket_status",None)
        ticket_priority = request.GET.get("ticket_priority",None)
        tickets = paginate(objects=tickets, per_page=12, page=request.GET.get("page"))
        self.ctx = {
            'statuses':Ticket.STATUSES,
            'types':Ticket.TYPES,
            'priorities':Ticket.PRIORITIES,
            'tickets':tickets
        }
        return render(request, self.template_name, self.ctx)

    def post(self, request, *args, **kwargs):
        from main.core.utils import generate_ticket_name

        ticket_desc = request.POST.get("description_in")
        ticket_subject = request.POST.get("subject_in")
        ticket_priority = request.POST.get("prec_in")
        ticket_type = request.POST.get("category_in")
        ob = Ticket.objects.create(
            user=request.user,
            ticket_name=generate_ticket_name(),
            ticket_desc=ticket_desc,
            ticket_subject=ticket_subject,
            ticket_priority=ticket_priority,
            ticket_type=ticket_type,
        )
        messages.success(request, _("Great Job, Your ticket has been created successfully"))
        self.ctx = {
            'statuses':Ticket.STATUSES,
            'types':Ticket.TYPES,
            'priorities':Ticket.PRIORITIES,
        }
        return render(request, self.template_name, self.ctx)

class TicketDetail(View):
    template_name = 'ticket/ticket_detail.html'
    ctx = {}

    def get(self, request, *args, **kwargs):
        ticket_id = int(request.resolver_match.kwargs.get('id'))
        ticket = get_object_or_404(Ticket, pk=ticket_id, user=request.user)
        answers = TicketMessage.objects.filter(user=request.user,ticket=ticket)
        message = request.GET.get("message")

        self.ctx = {
            'answers' : answers,
            'message'  : message,
            'ticket'   : ticket ,
        }
        return render(request,self.template_name, self.ctx)

    def post(self, request, *args, **kwargs):
        form = NewTicketForm(instance=request.user)
        message_ticket_id = int(request.resolver_match.kwargs.get('id'))
        ticket = get_object_or_404(Ticket, pk=message_ticket_id,user=request.user)
        message = request.POST.get("message")
        if message:
            if ticket.ticket_status == Ticket.OPEN:
                ob = TicketMessage.objects.create(
                    message = message,
                    user= request.user,
                    ticket=ticket,
                )
                ob.save()
                messages.success(request, _("Great Job, Your ticket message has been created successfully"))
            else:
                messages.error(request, _("ticket is closed ! "))



        else:
            display_form_validations(form, request, message_type=messages.ERROR)
        self.ctx = {
            'message'  : message,
            'ticket'   : ticket, 
        }
        return redirect('tickets:tickets_list_view')
         
        return render(request,self.template_name, self.ctx)

class NewTicket(View):
    template_name = 'ticket/new_ticket.html'
    ctx = {}

    def get(self, request, *args, **kwargs):
        self.ctx = {
            'statuses':Ticket.STATUSES,
            'types':Ticket.TYPES,
            'priorities':Ticket.PRIORITIES,
        }
        return render(request, self.template_name, self.ctx)

    def post(self, request, *args, **kwargs):
        form = NewTicketForm(instance=request.user)
        from main.core.utils import generate_ticket_name

        ticket_desc = request.POST.get("ticket_desc")
        ticket_subject = request.POST.get("ticket_subject")
        ticket_priority = request.POST.get("ticket_priority")
        ticket_type = request.POST.get("ticket_types")
        form.is_valid()
        ob = Ticket.objects.create(
            user=request.user,
            ticket_name=generate_ticket_name(),
            ticket_desc=ticket_desc,
            ticket_subject=ticket_subject,
            ticket_priority=ticket_priority,
            ticket_type=ticket_type,
        )
        ob.save()
        messages.success(request, _("Great Job, Your ticket has been created successfully"))
        self.ctx = {
            'statuses':Ticket.STATUSES,
            'types':Ticket.TYPES,
            'priorities':Ticket.PRIORITIES,
        }
        return redirect('tickets:tickets_list_view')

        return render(request, self.template_name, self.ctx)