from django.utils.translation import ugettext as _

from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.conf import settings
from collections import OrderedDict
from main.core.api import APIViewBase

class ResellerRouteView(APIViewBase):
    """
Reseller Route View
"""
    def get(self, request, *args, **kwargs):
        response = {
           "Reseller Locations Template Route"  : reverse(viewname="api:location_route_view" , request=request),
           "Reseller Categories Route"          : reverse(viewname="api:category_route_view" , request=request),
           "Reseller Branches Route"            : reverse(viewname="api:branch_route_view"   , request=request), 
           "Reseller Companies Route"           : reverse(viewname="api:company_route_view"  , request=request),
           "Reseller Product Template Route"    : reverse(viewname="api:template_route_view" , request=request),
           "Reseller Product Route "            : reverse(viewname="api:product_route_view"  , request=request),
           #"Reseller Products Favourites"       : reverse(viewname="api:favorite_route_view" , request=request),
           "Reseller Products Comments"         : reverse(viewname="api:product_comment_view", request=request), 
        } if settings.DISPLAY_API_ROOT else {}
        return Response(OrderedDict(sorted(response.items())))
    def get_view_name(self):
        return "Reseller Route"

