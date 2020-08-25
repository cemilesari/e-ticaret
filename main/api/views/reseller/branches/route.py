from django.utils.translation import ugettext as _

from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.conf import settings
from collections import OrderedDict
from main.core.api import APIViewBase


class BranchRouteView(APIViewBase):
    """
Reseller Branch Route View
"""
    def get(self, request, *args, **kwargs):
        response = {
            "Reseller Branch List Route " : reverse(viewname="api:branch_list_view" , request=request),
            "Reseller Branch Create View" : reverse(viewname="api:branch_create_view",request=request),
            
        } if settings.DISPLAY_API_ROOT else {}
        return Response(OrderedDict(sorted(response.items())))
    def get_view_name(self):
        return "Reseller Branch Route"

