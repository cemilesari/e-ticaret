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
from django.forms.models import model_to_dict
from django.http import HttpResponse
import json
from rest_framework import serializers
from rest_framework import viewsets

from main.api.serializers.reseller.product import ProductSerializer,ProductSerializerHYPER
class CompanyListAPIView(ListAPIView):
    serializer_class = CompanyViewSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user', 'city']
    pagination_class = CompanyPagination
    def get_queryset(self):
        queryset = Company.objects.filter(is_deleted=False)
        print(queryset)
        return queryset

class CompanyDetailAPIView(DestroyModelMixin,RetrieveAPIView,RetrieveUpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'pk'
    permission_classes = [IsOwner]
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
#class CompanyDetailAPIView(APIView):
#    """
#    Retrieve, update or delete a snippet instance.
#    """
#    def get_object(self, pk):
#        try:
#            return Company.objects.get(pk=pk)
#        except Company.DoesNotExist:
#            raise Http404
#
#    def get(self, request, pk, format=None):
#        company = self.get_object(pk)
#        print(company)
#        serializer = CompanyUCViewSerializer(company,context={'request': request} )
#        
#        return Response(serializer.data)
#
#    def put(self, request, pk, format=None):
#        company = self.get_object(pk)
#        serializer = CompanyUCViewSerializer(company, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#    def delete(self, request, pk, format=None):
#        company = self.get_object(pk)
#        company.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)

class CompanyCreateAPIView(CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyUCViewSerializer
    permission_classes =  [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

#class CompanyProductsAPIView(ListAPIView):
#    serializer_class = ProductSerializer
#    filter_backends = [SearchFilter, OrderingFilter]
#    pagination_class = CompanyPagination
#    def get_queryset(self):
#        queryset = Company.objects.filter(is_deleted=False)
#        print(queryset)
#        return queryset
#    def get_products(self):
#        if companies:
#            for com in companies:
#                print(com.id)
#                product = Product.objects.all()
#                for pro in product:
#                    if pro.template.company.id == com.id:
#                        print(com.name)
#                        p = []
#                        print("ben p list")
#                        p.append(com)
#                        print(p)                
#                    else:
#                        print("çalışmıyom ya ")
#        return p