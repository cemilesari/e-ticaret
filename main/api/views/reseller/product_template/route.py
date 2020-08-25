from django.utils.translation import ugettext as _

from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.conf import settings
from collections import OrderedDict
from main.core.api import APIViewBase


class TemplateRouteView(APIViewBase):
    """
Reseller Product Template Route View
"""
    def get(self, request, *args, **kwargs):
        response = {
            "Reseller Product List Route " : reverse(viewname="api:product_template_list" , request=request),
            "Reseller Product Create View" : reverse(viewname="api:product_template_create",request=request),
            #"Reseller Product Delete View" : reverse(viewname="api:product_create_view",request=request),
            #"Reseller Product Update View" : reverse(viewname="api:product_create_view",request=request),
        } if settings.DISPLAY_API_ROOT else {}
        return Response(OrderedDict(sorted(response.items())))
    def get_view_name(self):
        return "Reseller Product Template Route"

