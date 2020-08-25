
from __future__ import unicode_literals, absolute_import
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from main.order.models import Product, Location, Company, Branch, Category, ProductTemplate
from django.conf import settings


class LocationForm(ModelForm):
    class Meta :
        model = Location
        fields = ['address','city','state','country','zipcode','lati','lngt','mob','tel','fax','url','mail','tax_id','tax_branch']

