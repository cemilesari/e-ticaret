from django.utils.translation import ugettext as _

from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings

class APIViewBase(APIView):
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer,) if settings.DEBUG else (JSONRenderer,)
    def get(self, request, *args, **kwargs):
        return Response(dict(response="GET method not allowed"))