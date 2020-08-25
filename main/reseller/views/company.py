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
from main.reseller.forms import CompanyForm
from main.core.models import Currency
from main.reseller.forms import LocationForm
from django.views.decorators.csrf import csrf_exempt   
from django.utils.decorators import method_decorator
from main.core.utils import user_event

class CompanyView(View):
    template_name = 'reseller/company/company-list.html'
    ctx = {}
    def get(self, request, *args, **kwargs):
        companies = Company.objects.filter( user=request.user , is_deleted = False)

       
        name        = request.POST.get("name" , None)
        body        = request.POST.get("body" , None)
        logo         = request.POST.get("logo", None)
        size         = request.POST.get("size", None)
        category     = request.POST.get("category", None)
        location     = request.POST.get("location", None) 
        self.ctx ={
            'companies' : companies,
            'size'      : Company.SIZES,
            'category'  : Company.CATEGORIES,

        }
        return render(request, self.template_name, self.ctx)
    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, self.ctx)

class CompanyDetail(View):
    template_name = 'reseller/company/company-detail.html'
    ctx = {}

    def get(self, request, *args, **kwargs):
        company_id = int(request.resolver_match.kwargs.get('pk'))
        company = get_object_or_404(Company, pk=company_id, user=request.user)
        self.ctx = {
            'company' : company,
        }
        return render(request, self.template_name, self.ctx)
    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, self.ctx)

class NewCompany(View):
    template_name = 'reseller/company/newcompany.html'
    ctx = {}
    def get(self, request, *args, **kwargs):
        self.ctx = {
            'sizes' : Company.SIZES,
            'categories' : Company.CATEGORIES,
            'locations'   : Location.objects.filter(user=request.user, is_deleted = False)
        }
        return render(request, self.template_name, self.ctx)
    def post(self, request, *args, **kwargs):
        form = CompanyForm(instance=request.user)
        name         = request.POST.get("name") 
        body         = request.POST.get("body")
        logo         = request.FILES.get("logo")
        size         = request.POST.get("size")
        category     = request.POST.get("category")
        location     = request.POST.get("location")
        form.is_valid()
        obj = Company.objects.create(
            user       = request.user,
            name       = name or "Untiteled Company Name",
            body       = body,
            logo       = logo,
            size       = size,
            category   = category or Company.RESTAURANT,
            location   = Location.objects.get(pk=location),
            )
        obj.save()
        print(obj)
        print("-----------------------------------")
        print("-----------------------------------")
        print(logo)
        print("-----------------------------------")
        messages.success(request, _("Greet Job, Your Company has been created succesfully "))
        self.ctx = {
            'sizes'       : Company.SIZES,
            'categories'  : Company.CATEGORIES,
            'locations'   : Location.objects.filter(user=request.user, is_deleted = False)
        }
        return redirect('reseller:company_list')
        return render(request, self.template_name, self.ctx)
class DeleteCompanyView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"status":"method not allowed"})

    def post(self, request, *args, **kwargs):
        status = None
        company_id = request.POST.get('id')
        if company_id == 'all' :
            ob = Company.objects.filter(user=request.user, is_deleted = False)
            ob.update(is_deleted=True)
            ob.save()
            user_event(log_name="Delete All Addresses",log_text="{} Has Just Delete all address ,user : {}".format(request.user.username), user=request.user)            
            status = True
        else : 
            obj = get_object_or_404(Company, pk = company_id, user=request.user)
            obj.is_deleted = True
            obj.save()
            user_event(log_name="Delete Address",log_text="{} Has Just Delete one address ,address pk : {}".format(request.user.username, obj.id), user=request.user)            
            status = True
        return JsonResponse({"status" : status })
class UpdateCompanyView(UpdateView):
    model = Company
    template_name = 'reseller/company/company-update.html'
    context_object_name = "company"
    fields = ('name','body','logo','size','category','location',)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["locations"] = Location.objects.filter(user=user , is_deleted = False)
        return context
    def get_success_url(self):
        return reverse_lazy('reseller:detail_company', kwargs={'pk': self.object.id})
