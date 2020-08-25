from __future__ import unicode_literals, absolute_import
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from main.order.models import Product, Location, Company, Branch, Category, ProductTemplate
from django.conf import settings

from django import forms
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['branch','template','left','count','user','original_price','price','start_time','end_time','sold_time','status','is_deleted',]
        widgets = {
            'start_time': forms.TimeInput(format=['%H:%M']),
            'end_time': forms.TimeInput(format=['%H:%M']),
            'sold_time': forms.TimeInput(format=['%H:%M']),
         }
