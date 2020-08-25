from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (ListAPIView, 
                                    RetrieveAPIView, 
                                    DestroyAPIView, 
                                    RetrieveUpdateAPIView , 
                                    CreateAPIView, )
from main.order.models import Company,Product
from main.api.serializers.reseller.companies import CompanySerializer,CompanyViewSerializer,CompanyUCViewSerializer
from rest_framework.permissions import IsAuthenticated
from main.api.permissions import IsOwner
from main.api.paginations import *
from rest_framework.mixins import DestroyModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
import json
from rest_framework import serializers
from rest_framework import viewsets

from main.api.serializers.reseller.product import ProductSerializer,ProductSerializerHYPER
class CompanyDetailProductAPIView(ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['branch', 'template']
    pagination_class = ProductPagination
    def get_object(self, pk):
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            raise Http404
    def get_queryset(self):
        company=Company.objects.all()
        for comp in company:
            queryset = Product.objects.filter(is_deleted=False, template__company_id=comp.id)
        return queryset
       