# -*- encoding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.shortcuts import HttpResponseRedirect, render, redirect, HttpResponse, get_object_or_404
from django.http import JsonResponse, Http404
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django.urls import reverse_lazy
from django.views import View
from main.order.models import Branch, Product, ProductTemplate, Location, Category, Company
from main.users.models import User
from datetime import datetime, timedelta

#https://docs.djangoproject.com/en/2.2/_modules/django/views/generic/dates/
#mixin date week 

class ProfileView(View):
    template_name="reseller/includes/profile/profile_view.html"
    ctx = {}

    def get(self, request, *args, **kwargs):
        one_week_ago = datetime.today() - timedelta(days=7)
        one_day_ago  = datetime.today() - timedelta(days=1)
        one_year_ago = datetime.today() - timedelta(weeks=54)
        
        locations = Location.objects.filter(user=request.user, is_deleted=False)
        companies = Company.objects.filter(user=request.user, is_deleted=False) 
        branches  = Branch.objects.filter(user=request.user, is_deleted=False)
        templates = ProductTemplate.objects.filter(user=request.user, is_deleted=False)
        products = Product.objects.filter(user=request.user, is_deleted= False)
        product_week = Product.objects.filter(created__gte=one_week_ago,user=request.user, is_deleted= False)
        product_day  = Product.objects.filter(created__gte=one_day_ago,user=request.user, is_deleted= False)
        product_year = Product.objects.filter(created__gte=one_year_ago,user=request.user, is_deleted= False)
        self.ctx = {
            'locations' : locations,
            'companies' : companies,
            'branches'  : branches,
            'templates' : templates,
            'products'  : products,
            'product_week' : product_week,
            'product_day' : product_day,
            'product_year' : product_year,
        }
        return render(request, self.template_name, self.ctx)
    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, self.ctx)        

