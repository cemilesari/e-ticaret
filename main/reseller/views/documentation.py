
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
from django.views import View
from main.core.utils import paginate,str2date
from main.order.models import Branch, Product, ProductTemplate, Location, Category, Company
from main.users.models import User
from main.reseller.forms import CompanyForm, BranchFrom
from main.core.models import Currency
from main.reseller.forms import LocationForm
from django.views.decorators.csrf import csrf_exempt   
from django.utils.decorators import method_decorator
from main.core.utils import user_event

class DocumentationView(View):
    template_name = 'reseller/documents/documentationapi.html'
    ctx = {}

    def get(self, request, *args, **kwargs):
        branches = Branch.objects.filter(user=request.user, is_deleted = False)
        name     = request.GET.get("name" , None)
        body     = request.GET.get("body" , None)
        user     = request.GET.get("user" , None)
        location = request.GET.get("location", None)
        company  = request.GET.get("company" , None)
        self.ctx = {
            'branches'  : branches 
        }
        return render(request, self.template_name, self.ctx)
    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, self.ctx)

        