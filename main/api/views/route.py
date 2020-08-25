from django.utils.translation import ugettext as _

from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.conf import settings
from collections import OrderedDict
from main.core.api import APIViewBase

class MainRouteView(APIViewBase):
    """
Main Route View
"""
    def get(self, request, *args, **kwargs):
        response = {
            "Authentication Route":       reverse(viewname="api:auth_route_view",        request=request),
            "Consumer Route"      :       reverse(viewname="api:consumer_route_view",    request=request),
			"Reseller Route"      :       reverse(viewname="api:reseller_route_view",    request=request),
            "User Route"          :       reverse(viewname="api:user_route_view",        request=request),
        } if settings.DISPLAY_API_ROOT else {}
        return Response(OrderedDict(sorted(response.items())))
    def get_view_name(self):
        return "Main Route"