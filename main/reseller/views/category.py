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
from main.order.models import Category
from main.users.models import User
from main.reseller.forms import CategoryForm
from main.order.models import Product

class CategoryListView(ListView):
    template_name = 'reseller/category/categories.html'
    ctx = {}
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        self.ctx ={
            'categories' : categories,
        }
        print(categories)
        return render(request, self.template_name, self.ctx)
    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, self.ctx)
class NewCategoryView(View):
    template_name = 'reseller/category/newcategory.html'
    ctx = {}
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.ctx)
    def post(self, request, *args, **kwargs):
        form = CategoryForm()
        name = request.POST.get("name")
        form.is_valid()
        obj = Category.objects.create(
            name=name,
            )
        obj.save()
        messages.success(request, _("Greet Job, Your category has been created succesfully "))
        return redirect('reseller:category_view')
        return render(request, self.template_name, self.ctx)


class DetailCategory(View):
    template_name = 'reseller/category/category-product.html'
    ctx = {}
    def get(self, request, *args, **kwargs):
        category_id = int(request.resolver_match.kwargs.get('pk'))
        category    = get_object_or_404(Category, pk = category_id )
        products    = Product.objects.all()
        self.ctx = {
            'category' : category,
            'products' : products,
        }
        return render(request, self.template_name, self.ctx)
    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, self.ctx)
