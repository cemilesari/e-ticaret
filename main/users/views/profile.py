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

from main.core.utils import paginate,str2date
from main.order.models import Branch, Product, ProductTemplate, Location, Category, Company
from main.users.models import User
from main.reseller.forms import ProductForm
from main.core.models import Currency



class ProfileView(ListView):
	model = User
	template_name = 'auth/profile.html'
	context_object_name = "users"
	paginete_by = 5
	def get_context_data(self, **kwargs):
		context = super(ProfileView, self).get_context_data(**kwargs)
		products = self.get_queryset()
		products = paginate(
			objects=products, 
			per_page=6, 
			page=self.request.GET.get("page"))
		
		context['products'] = products
		return context 