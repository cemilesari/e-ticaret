from django.utils.translation import ugettext as _

from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.conf import settings
from collections import OrderedDict
from main.core.api import APIViewBase

class AuthRouteView(APIViewBase):
    """
Authentication Route View
"""
    def get(self, request, *args, **kwargs):
        response = {
            "Token Obtain Pair": reverse(viewname="api:token_obtain_pair", request=request),
            "Token Refresh": reverse(viewname="api:token_refresh", request=request),
            "Token Verify": reverse(viewname="api:token_verify", request=request),
        } if settings.DISPLAY_API_ROOT else {}
        return Response(OrderedDict(sorted(response.items())))
    def get_view_name(self):
        return "Authentication Route"