from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (ListAPIView, 
                                    RetrieveAPIView, 
                                    DestroyAPIView, 
                                    RetrieveUpdateAPIView , 
                                    CreateAPIView, )
from main.order.models import Product, ProductTemplate
from main.api.serializers.reseller.product import ProductSerializer ,ProductUCSerializer
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated

from main.api.permissions import IsOwner
from main.api.paginations import *

class ProductListAPIView(ListAPIView):
    #queryset = Product.objects.all()
    serializer_class = ProductSerializer
    #searchs
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['branch', 'template']
    pagination_class = ProductPagination
    def get_queryset(self):
        queryset = Product.objects.filter(is_deleted=False)
        return queryset
class ProductDetailAPIView(DestroyModelMixin,RetrieveAPIView,RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductUCSerializer
    lookup_field = 'pk'
    permission_classes = [IsOwner]
    #delete button ussed to DestroyModelMixin
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ProductCreateAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductUCSerializer
    permission_classes =  [IsAuthenticated]
    #serializer save used , changes
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


#class ProductDeleteAPIView(DestroyAPIView):
#    queryset = Product.objects.all()
#    serializer_class = ProductSerializer
#    lookup_field = 'pk'
#    permission_classes = [IsOwner]
#class ProductUpdateAPIView(DestroyModelMixin, RetrieveUpdateAPIView):
#    queryset = Product.objects.all()
#    serializer_class = ProductUCSerializer
#    lookup_field = 'pk'
#    permission_classes = [IsOwner]
#    #delete button ussed to DestroyModelMixin
#    def delete(self, request, *args, **kwargs):
#        return self.destroy(request, *args, **kwargs)



#class ProductListAPIView(ListAPIView, CreateModelMixin):
#    #queryset = Product.objects.all()
#    serializer_class = ProductUCSerializer
#    #searchs
#    filter_backends = [SearchFilter,OrderingFilter]
#    search_fields = ['branch', 'template']
#    pagination_class = ProductPagination
#    def get_queryset(self):
#        queryset = Product.objects.filter(is_deleted=False)
#        return queryset
#    def post(self, request, *args, **kwargs):
#        return self.create(request, *args, **kwargs)
#    def perform_create(self, serializer):
#        serializer.save(user = self.request.user)