from django.utils.translation import ugettext as _

from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.conf import settings
from collections import OrderedDict
from main.core.api import APIViewBase

class UserRouteView(APIViewBase):
    """
User Route View
"""
    def get(self, request, *args, **kwargs):
        response = {
            "User List Route "             : reverse(viewname="api:user_list_view"   , request=request),
            "Product List For User Route " : reverse(viewname="api:user-for-product" , request=request),

        } if settings.DISPLAY_API_ROOT else {}
        return Response(OrderedDict(sorted(response.items())))
    def get_view_name(self):
        return "User Route"

