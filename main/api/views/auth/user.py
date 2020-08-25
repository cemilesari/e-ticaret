from django.utils.translation import ugettext as _
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.db.models import Max
from rest_framework.generics import CreateAPIView

from django.conf import settings
from collections import OrderedDict

from main.users.models import User
from main.api.serializers.user import RegisterSerializer
class UserApiBase(APIView):
    rescode = 400
    result = {}
    error = None 
    error_message = None 
    permission_classes = (IsAuthenticated,)
    #renderer_classes = (BrowsableAPIRenderer, JSONRenderer,) if settings DEBUG else (JSONRenderer, )
    allowed_methods = ['POST' , 'GET']
    def get(self, request, *args, **kwargs):
        return Response(dict(response = "Get method not allowed"))

#class UserInfoAPI(UserAPIBase):
class UserInfoAPI(APIView):
    def get(self, request, *args, **kwargs):
        self.request = {
            'user_info' : UserSerializer(request.user).data, 

        }
        self.rescode = 200
        return Response(dict(result=self.result, error_message = self.error_message, error=self.error), status=self.rescode)
#access token token sunucuda kontrol ediliyor 
#refresh token


class RegisterSerializer(CreateAPIView):
    def get(self, request, *args, **kwargs):
        return Response(dict(response = "Get method not allowed"))
    def post(self, request, *args,**kwargs):
        serializer = RegistrationSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "succesfully registered a new user"
            data['email'] = user.email
            data['username'] = user.username
        else:
            data = serializer.errors
        return Response(data)