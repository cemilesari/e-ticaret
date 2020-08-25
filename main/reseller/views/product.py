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
from main.core.utils import get_query
from main.core.utils import paginate,user_event


class ProductListView(View):
	template_name = 'reseller/products/products.html'
	ctx = {}
	def get(self, request, *args, **kwargs):
		products = Product.objects.filter(user=request.user, is_deleted = False)
		search   = request.GET.get("search" , None)
		branch   = request.GET.get("branch",  None)
		template = request.GET.get("template",None)
		status   = request.GET.get("status",  None)
		if search:
			query_entry = get_query(search, ("branch__name", "template__name",))
			products = products.filter(query_entry)
		if template:
			query_entry = get_query(template, ("template__name",))
			products = products.filter(query_entry)
		if branch:
			query_entry = get_query(branch, ("branch__name",))
			products = products.filter(query_entry)
		if status:
			query_entry = get_query(status, ("status",))
			products = products.filter(query_entry)
		products = paginate(objects=products, per_page=5, page = request.GET.get("page"))
		self.ctx = {
			'products'  : products,
			'branch' : Branch.objects.filter(user=request.user,is_deleted = False),
			'template' : ProductTemplate.objects.filter(user=request.user, is_deleted = False),
			'status'  : Product.STATUSES,
		}
		return render(request, self.template_name, self.ctx)
	def post(self, request, *args, **kwargs):
		
		branch   = request.POST.get("branch" , None)
		template = request.POST.get("template", None)
		left     = request.POST.get("template" , None)
		count    = request.POST.get("count" , None)
		original_price = request.POST.get("original_price", None)
		price      = request.POST.get("price", None)
		start_time = request.POST.get("start_time", None)
		end_time   = request.POST.get("end_time", None)
		sold_time  = request.POST.get("sold_time" , None)
		status     = request.POST.get("status" , None)

		return render(request, self.template_name, self.ctx)


class ProductDetailView(View):
	template_name = 'reseller/products/product-detail.html'
	ctx = {}

	def get(self, request, *args, **kwargs):
		product_id = int(request.resolver_match.kwargs.get('pk'))
		product = get_object_or_404(Product, pk=product_id, user=request.user)
		self.ctx = {
			'product' : product,
		}
		return render(request, self.template_name, self.ctx)
	def post(self, request, *args, **kwargs):
		return render(request, self.template_name, self.ctx)


class ProductCreateView(View):
	template_name = 'reseller/products/new-product.html'
	ctx = {}
	def get(self, request, *args, **kwargs):
		self.ctx = {
			'branches'  :Branch.objects.filter(user=request.user, is_deleted = False),
			'templates' :ProductTemplate.objects.filter(user=request.user, is_deleted = False),
			'companies' :Company.objects.filter(user=request.user, is_deleted = False),
			'status'    :Product.STATUSES,
		}
		return render(request, self.template_name, self.ctx)
	def post(self, request, *args, **kwargs):
		form = ProductForm(instance = request.user)
		branch     		   = request.POST.get("branch")
		template     	   = request.POST.get("template")
		count              = request.POST.get("count")
		left               = request.POST.get("left")
		original_price     = request.POST.get("original_price")
		price              = request.POST.get("price")
		start_time         = request.POST.get("start_time")
		end_time           = request.POST.get("end_time")
		sold_time          = request.POST.get("sold_time")
		status             = request.POST.get("status")
		form.is_valid()
		obj = Product.objects.create(
			user = request.user,
			branch         = Branch.objects.get(pk=branch),
			template       = ProductTemplate.objects.get(pk=template),
			left           = left,
			count          = count,
			price          = price,
			original_price = original_price,
			start_time     = start_time,
			sold_time      = sold_time ,
			end_time       = end_time,
			status         = status,
			)
		obj.save()
		print(obj)
		messages.success(request, _("Greet Job, Your Branch has been created succesfully "))
		self.ctx = {
			'branches'  :Branch.objects.filter(user=request.user, is_deleted = False),
			'companies' :Company.objects.filter(user=request.user, is_deleted = False)
		}
		return redirect('reseller:product_list')
		return render(request, self.template_name, self.ctx)

class ProductDeleteView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"status":"method not allowed"})

    def post(self, request, *args, **kwargs):
        status = None
        product_id = request.POST.get('id')
        if product_id == 'all' :
            ob = Company.objects.filter(user=request.user, is_deleted = False)
            ob.update(is_deleted=True)
            ob.save()
            user_event(log_name="Delete All Products",log_text="{} Has Just Delete all products ,user : {}".format(request.user.username), user=request.user)            
            status = True
        else : 
            obj = get_object_or_404(Product, pk = product_id, user=request.user)
            obj.is_deleted = True
            obj.save()
            user_event(log_name="Delete Product",log_text="{} Has Just Delete one product ,address pk : {}".format(request.user.username, obj.id), user=request.user)            
            status = True
        return JsonResponse({"status" : status })

class ProductUpdateView(UpdateView):
	model = Product
	template_name ='reseller/products/update-product.html'
	context_object_name = "product"
	fields = ('branch','status','left','count','original_price','price','start_time','end_time','sold_time',)
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["branches"] = Branch.objects.filter(user=self.request.user)
		context["templates"] = ProductTemplate.objects.filter(user=self.request.user)
		return context
	def get_success_url(self):
		return reverse_lazy('reseller:detail_product', kwargs={'pk': self.object.id})
