from django.utils.translation import ugettext as _

from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.conf import settings
from collections import OrderedDict
from main.core.api import APIViewBase

class ConsumerRouteView(APIViewBase):
    """
Consumer Route View
"""
    def get(self, request, *args, **kwargs):
        response = {

        } if settings.DISPLAY_API_ROOT else {}
        return Response(OrderedDict(sorted(response.items())))
    def get_view_name(self):
        return "Consumer Route"