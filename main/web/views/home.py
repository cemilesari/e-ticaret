# -*- encoding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.shortcuts import HttpResponseRedirect, render, redirect, HttpResponse, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from main.order.models import Company
from datetime import datetime, timedelta

def global_manage(request):
	response = {}
	return JsonResponse(response, safe=True)


#Post.objects.order_by('created_date)- en sondan 
#başlayarak gösteririr....
#https://books.agiliq.com/projects/django-orm-cookbook/en/latest/aggregation.html
#User.objects.all().aggregate(Max('id'))
#Post.objects.filter(published_date__lte = timezone.now()).order_by('published_date')

class BestSellers(View):
	template_name = 'web/home.html'
	ctx = {}

	def get(self, request, *args, **kwargs):
		one_week_ago = datetime.today() - timedelta(days=7)
		one_day_ago  = datetime.today() - timedelta(days=1)
		one_year_ago = datetime.today() - timedelta(weeks=54)
		companies = Company.objects.all()[:3]
		#companies1 = Company.objects.all()[3:6]
		count   = Company.objects.all().count()
		companies_week = Company.objects.filter(created__gte=one_week_ago, is_deleted= False)
		companies_day  = Company.objects.filter(created__gte=one_day_ago,  is_deleted= False)
		companies_year = Company.objects.filter(created__gte=one_year_ago, is_deleted= False)[:3]
		self.ctx = {
			'companies_week' : companies_week,
			'companies_day' : companies_day,
			'companies_year' : companies_year,
			'companies' : companies,
			'count'     : count,
		}
		return render(request, self.template_name, self.ctx)
	def post(self, request,*args, **kwargs):
		return render(request, self.template_name, self.ctx)
#company count --> all().count