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
from main.reseller.forms import ProductForm
from main.core.models import Currency
from main.reseller.forms import LocationForm
from django.views.decorators.csrf import csrf_exempt   
from django.utils.decorators import method_decorator
from main.core.utils import user_event

class AddresseView(View):
    template_name = 'reseller/addresse/addresse-view.html'
    ctx = {}
    def get(self, request, *args, **kwargs):
        ads = Location.objects.filter( user=request.user, is_deleted=False)
        self.ctx ={
            'ads' : ads,
        }
        print(ads)
        return render(request, self.template_name, self.ctx)
    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, self.ctx)

class AddresseDetail(View):
    template_name = 'reseller/addresse/addresse-detail.html'
    ctx = {}

    def get(self, request, *args, **kwargs):
        address_id = int(request.resolver_match.kwargs.get('pk'))
        address = get_object_or_404(Location, pk=address_id, user=request.user)
        self.ctx = {
            'address' : address,
        }
        return render(request, self.template_name, self.ctx)
    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, self.ctx)

class NewAddresse(View):
    template_name = 'reseller/addresse/addresse-create.html'
    ctx = {}
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.ctx)
    def post(self, request, *args, **kwargs):
        form = LocationForm(instance=request.user)
        address      = request.POST.get("address") 
        city         = request.POST.get("city")
        state        = request.POST.get("state")
        country      = request.POST.get("country")
        zipcode      = request.POST.get("zipcode")
        lati         = request.POST.get("lati")
        lngt         = request.POST.get("lngt")
        mob          = request.POST.get("mob")
        tel          = request.POST.get("tel")
        fax          = request.POST.get("fax")
        url          = request.POST.get("url")
        mail         = request.POST.get("mail")
        tax_id       = request.POST.get("tax_id")
        tax_branch   = request.POST.get("tax_branch")
        form.is_valid()
        obj = Location.objects.create(
            user = request.user,
            address    = address,
            city       = city,
            state      = state,
            country    = country,
            zipcode    = zipcode,
            lati       = lati,
            lngt       = lngt,
            mob        = mob,
            tel        = tel,
            fax        = fax,
            url        = url,
            mail       = mail,
            tax_id     = tax_id,
            tax_branch = tax_branch,  
        )
        obj.save()
        messages.success(request, _("Greet Job, Your location address has been created succesfully "))
        return redirect('reseller:addresse_view')
        return render(request, self.template_name, self.ctx)

class DeleteAddresseView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"status":"method not allowed"})

    def post(self, request, *args, **kwargs):
        status = None
        address_id = request.POST.get('id')
        if address_id == 'all' :
            ob = Location.objects.filter(user=request.user, is_deleted = False)
            ob.update(is_deleted=True)
            ob.save()
            user_event(log_name="Delete All Addresses",log_text="{} Has Just Delete all address ,user : {}".format(request.user.username), user=request.user)            
            status = True
        else : 
            obj = get_object_or_404(Location, pk = address_id, user=request.user)
            obj.is_deleted = True
            obj.save()
            print(obj.is_deleted)
            user_event(log_name="Delete Address",log_text="{} Has Just Delete one address ,address pk : {}".format(request.user.username, obj.id), user=request.user)            
            status = True
            print(status)
        return JsonResponse({"status" : status })
class UpdateAddresseView(UpdateView):
    model = Location
    template_name = 'reseller/addresse/addresse-update.html'
    context_object_name = "address"
    fields = ('address','city','state','country','zipcode','lati','lngt','mob','tel','fax','url','mail','tax_id','tax_branch',)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def get_success_url(self):
        return reverse_lazy('reseller:addresse-detail', kwargs={'pk': self.object.id})
    
