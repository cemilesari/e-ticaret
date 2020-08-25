from __future__ import unicode_literals, absolute_import
from django.utils.translation import ugettext_lazy as _ 
from django import forms
from main.users.models import User
from main.order.models import ProductTemplate
from django.core.validators import MaxLengthValidator, MinLengthValidator, EmailValidator

class ProductTemplateForm(forms.ModelForm):
    class Meta : 
        model = ProductTemplate
        fields = ('name','body','image','left','count','user','category','company','original_price','price','currency','status',)