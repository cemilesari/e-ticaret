from django.utils.translation import ugettext as _

from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.conf import settings
from collections import OrderedDict
from main.core.api import APIViewBase


class CategoryRouteView(APIViewBase):
    """
Reseller Category Route View
"""
    def get(self, request, *args, **kwargs):
        response = {
            "Reseller Category List Route " : reverse(viewname="api:category_list_view" , request=request),
            "Reseller Category Create View" : reverse(viewname="api:category_create_view",request=request),
        } if settings.DISPLAY_API_ROOT else {}
        return Response(OrderedDict(sorted(response.items())))
    def get_view_name(self):
        return "Reseller Category Route"

