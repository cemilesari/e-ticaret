from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (ListAPIView, 
                                    RetrieveAPIView, 
                                    DestroyAPIView, 
                                    RetrieveUpdateAPIView , 
                                    CreateAPIView,
                                    UpdateAPIView )
from rest_framework.views import APIView
from django.db.models import Q
from django.db.models.functions import Radians, Power, Sin, Cos, ATan2, Sqrt, Radians
from django.db.models import F
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from main.api.permissions import IsOwner
from main.api.paginations import *
from main.api.serializers.user import *
from main.users.models import User
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin
from main.api.serializers.reseller.product import ProductSerializer
from main.api.serializers.user import ChangePasswordSerializer
from rest_framework.response import Response
from django.contrib.auth import update_session_auth_hash
from main.api.permissions import NotAuthenticated
from main.api.throttles import RegisterThrottle
from main.order.models.product import Product
class UserListView(ListAPIView):
    serializer_class = UserSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['username', 'full_name']
    pagination_class = UserPagination
    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

#update-->put
class UpdatePassword(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            update_session_auth_hash(request,self.object)
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationDetailAPIView(DestroyModelMixin,RetrieveAPIView,RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerDetail
    lookup_field = 'pk'
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


#create user
class CreateUserView(CreateAPIView):
    throttle_classes =  [RegisterThrottle]
    model = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [NotAuthenticated]



class LocationDetailForAPIView(ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    pagination_class = ProductPagination
    def get_queryset(self):
        dlat = Radians(F('branch__location__lati')  - self.request.user.lati)
        dlong = Radians(F('branch__location__lngt') - self.request.user.lngt)
        a = (Power(Sin(dlat/2), 2) + Cos(Radians(self.request.user.lati)) 
            * Cos(Radians(F('branch__location__lati'))) * Power(Sin(dlong/2), 2)
            )
        c = 2 * ATan2(Sqrt(a), Sqrt(1-a))
        d = 6371 * c
        queryset = Product.objects.annotate(distance=d).order_by('distance').filter(distance__lt=50)[:50]
        return queryset
        #lngt1 = self.request.user.lngt - 5
        #lati1 = self.request.user.lati - 5
        #lngt11 = self.request.user.lngt - 5
        #lati11 = self.request.user.lati - 5
        #queryset = Product.objects.filter(
        #    Q(branch__location__lngt__gte=int(lngt1) , branch__location__lngt__lte=int(lngt11))).filter(
        #    Q(branch__location__lati__gte=int(lati1) , branch__location__lati__lte=int(lati11)))
        #print(queryset)
        #return queryset