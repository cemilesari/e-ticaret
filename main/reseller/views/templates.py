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
from main.reseller.forms import ProductTemplateForm
from main.core.models import Currency
from django.views.decorators.csrf import csrf_exempt   
from django.utils.decorators import method_decorator
from main.core.utils import user_event

class TemplatesList(View):
    template_name = 'reseller/product-template/template-list.html'
    ctx = {}
    def get(self, request, *args, **kwargs):
        templates = ProductTemplate.objects.filter( user=request.user , is_deleted = False)
        name               = request.POST.get("name" , None)
        body               = request.POST.get("body" , None)
        image              = request.FILES.get("image", None)
        left               = request.POST.get("left", None)
        count              = request.POST.get("count", None)
        price              = request.POST.get("price", None)
        original_price     = request.POST.get("original_price", None)
        category           = request.POST.get("category", None)
        currency           = request.POST.get("curency", None)
        status             = request.POST.get("status", None) 
        self.ctx ={
            'templates'   : templates,
            'currencies'  : ProductTemplate.CURRENCIES,
            'statuses'    : ProductTemplate.STATUSES,
        }
        return render(request, self.template_name, self.ctx)
    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, self.ctx)

class TemplatesDetail(View):
    template_name = 'reseller/product-template/template-detail.html'
    ctx = {}

    def get(self, request, *args, **kwargs):
        template_id = int(request.resolver_match.kwargs.get('pk'))
        template = get_object_or_404(ProductTemplate, pk=template_id, user=request.user)
        self.ctx = {
            'template' : template,
        }
        return render(request, self.template_name, self.ctx)
    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, self.ctx)

class TemplatesCreate(View):
    template_name = 'reseller/product-template/template-create.html'
    ctx = {}
    def get(self, request, *args, **kwargs):
        self.ctx = {
            'currencies'    : ProductTemplate.CURRENCIES,
            'statuses'      : ProductTemplate.STATUSES,
            'companies'     : Company.objects.filter(user=request.user, is_deleted = False),
            'categories'    : Category.objects.all(),
        }
        return render(request, self.template_name, self.ctx)
    def post(self, request, *args, **kwargs):
        form = ProductTemplateForm(instance=request.user)
        name               = request.POST.get("name" , None)
        body               = request.POST.get("body" , None)
        image              = request.FILES.get("image", None)
        left               = request.POST.get("left", None)
        count              = request.POST.get("count", None)
        price              = request.POST.get("price", None)
        original_price     = request.POST.get("original_price", None)
        company            = request.POST.get("company" , None)
        currency           = request.POST.get("currency", None)
        category           = request.POST.get("category", None)
        status             = request.POST.get("status", None) 
        form.is_valid()
        obj = ProductTemplate.objects.create(
            name           = name or "Untiteled ProductTemplate Name",
            body           = body,
            user           = request.user,
            left           = left,
            count          = count,
            image          = image,
            category       = Category.objects.get(pk=category),
            company        = Company.objects.get(pk=company),
            original_price = original_price,
            price          = price,
            currency       = currency,
            status         = status ,
            )
        obj.save()
        messages.success(request, _("Greet Job, Your ProductTemplate has been created succesfully "))
        self.ctx = {
            'statuses'   : ProductTemplate.STATUSES,
            'currencies' : ProductTemplate.CURRENCIES,
            'companies'  : Company.objects.filter(user=request.user, is_deleted = False),
            'categories' : Category.objects.all(),

        }
        return redirect('reseller:template_list')
        return render(request, self.template_name, self.ctx)
class TemplatesDelete(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"status":"method not allowed"})

    def post(self, request, *args, **kwargs):
        status = None
        template_id = request.POST.get('id')
        if template_id == 'all' :
            ob = ProductTemplate.objects.filter(user=request.user, is_deleted = False)
            ob.update(is_deleted=True)
            ob.save()
            user_event(log_name="Delete All Addresses",log_text="{} Has Just Delete all address ,user : {}".format(request.user.username), user=request.user)            
            status = True
        else : 
            obj = get_object_or_404(ProductTemplate, pk = template_id, user=request.user)
            obj.is_deleted = True
            obj.save()
            user_event(log_name="Delete Address",log_text="{} Has Just Delete one address ,address pk : {}".format(request.user.username, obj.id), user=request.user)            
            status = True
        return JsonResponse({"status" : status })
class TemplatesUpdate(UpdateView):
    model = ProductTemplate
    template_name = 'reseller/product-template/template-update.html'
    context_object_name = "template"
    fields = ('name','body','image','left','count','user','category','company','original_price','price','currency','status',)    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["categories"] = Category.objects.all()
        context["companies"]  = Company.objects.filter(user=user, is_deleted = False)
        return context
    def get_success_url(self):
        return reverse_lazy('reseller:template_detail', kwargs={'pk': self.object.id})
