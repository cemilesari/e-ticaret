from django.contrib import admin
from django.conf import settings 
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth.decorators import login_required

from .views import *

app_name = 'tickets'

urlpatterns = [
    path('', view=login_required(TicketView.as_view()), name = "tickets_list_view"),
    path('ticket-detail/<int:id>/', view=login_required(TicketDetail.as_view()), name="ticket_detail_view"),
    path('new_ticket/', view=login_required(NewTicket.as_view()), name="new_ticket"),
    path('<int:id>/ticket_message/', view=login_required(TicketDetail.as_view()), name="ticket_message"),
]