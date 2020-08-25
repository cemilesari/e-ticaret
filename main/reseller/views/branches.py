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

class BranchesView(View):
    template_name = 'reseller/branches/branch-list.html'
    ctx = {}

    def get(self, request, *args, **kwargs):
        branches = Branch.objects.filter(user=request.user, is_deleted = False)
        name = request.GET.get("name" , None)
        body = request.GET.get("body", None)
        user = request.GET.get("user", None)
        location = request.GET.get("location" , None)
        company = request.GET.get("company" , None)
        self.ctx = {
            'branches'  : branches 
        }
        return render(request, self.template_name, self.ctx)
    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, self.ctx)

class BranchesDetail(View):
    template_name = 'reseller/branches/branch-detail.html'
    ctx = {}

    def get(self, request, *args, **kwargs):
        branch_id = int(request.resolver_match.kwargs.get('pk'))
        branch    = get_object_or_404(Branch, pk = branch_id , user = request.user)
        self.ctx = {
            'branch' : branch,
        }
        return render(request, self.template_name, self.ctx)
    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, self.ctx)

class NewBranch(View):
    template_name = 'reseller/branches/new-branch.html'
    ctx = {}

    def get(self, request, *args, **kwargs):
        self.ctx = {
            'companies' : Company.objects.filter(user=request.user, is_deleted = False),
            'locations' : Location.objects.filter(user=request.user, is_deleted = False),
        }
        return render(request, self.template_name, self.ctx)
    def post(self, request,*args, **kwargs):
        form = BranchFrom(instance=request.user)
        name     = request.POST.get("name", None)  
        body     = request.POST.get("body", None)
        company  = request.POST.get("company", None)
        location = request.POST.get("location", None)
        form.is_valid()
        obj = Branch.objects.create(
            user = request.user,
            name = name or "Untiteled Branch Name",
            body = body, 
            company  = Company.objects.get(pk= company),
            location = Location.objects.get(pk=location)
        )
        obj.save()
        messages.success(request, _("Greet Job, Your Branch has been created succesfully "))
        self.ctx = {
            'locations' : Location.objects.filter(user=request.user, is_deleted = False), 
            'companies' : Company.objects.filter(user=request.user, is_deleted = False)
        }
        return redirect('reseller:branch_list')
        return render(request, self.template_name, self.ctx)

class DeleteBranch(View):
    template_name = 'reseller/branches/delete-branch.html'
    ctx = {}
    def get(self, request, *args, **kwargs):
        return JsonResponse({"status" : "method not allowed"})
    def post(self, request,*args, **kwargs):
        status = None
        branch_id = request.POST.get("id")
        if branch_id == 'all' :
            ob = Branch.objects.filter(user=request.user, is_deleted = False)
            ob.update(is_deleted = True)
            ob.save()
            user_event(log_name="Delete All Branches",log_text="{} Has Just Delete all branch ,user : {}".format(request.user.username), user=request.user)            
            status = True
        else : 
            obj = get_object_or_404(Branch, pk= branch_id, user = request.user)
            obj.is_deleted = True
            obj.save()
            user_event(log_name="Delete Branch",log_text="{} Has Just Delete one branch ,branch pk : {}".format(request.user.username, obj.id), user=request.user)            
            status = True
        return JsonResponse({"status" : status})
class UpdateBranch(UpdateView):
    model = Branch
    template_name = 'reseller/branches/update-branch.html'
    context_object_name = 'branch'
    fields = ('name','body','location',)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["locations"] = Location.objects.filter(user = user, is_deleted = False)
        context["users"]    =  User.objects.all()
        return context
    def get_success_url(self):
        return reverse_lazy('reseller:detail_branch' , kwargs={'pk':self.object.id})
