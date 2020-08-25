# -*- encoding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.shortcuts import HttpResponseRedirect, render, redirect, HttpResponse, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.views.generic.detail import DetailView 
from django.views.generic import ListView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views import View
from main.order.models import Branch, Product, ProductTemplate, Location, Category, Company
from main.users.models import User
from main.reseller.forms import ProductForm
from main.core.models import Currency
from main.reseller.forms import ProductForm

def home_view(request):
	return render(request, "reseller/home.html", {})
def global_manage(request):
	response = {}
	return JsonResponse(response, safe=True)