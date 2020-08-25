from __future__ import unicode_literals, absolute_import
from django.utils.translation import ugettext_lazy as _ 
from django import forms
from main.users.models import User
from main.order.models import Company
from django.core.validators import MaxLengthValidator, MinLengthValidator, EmailValidator

class CompanyForm(forms.ModelForm):
    class Meta : 
        model = Company
        fields = ('name','body','logo','user','size','category','location',)