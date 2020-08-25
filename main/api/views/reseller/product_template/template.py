from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (ListAPIView, 
                                    RetrieveAPIView, 
                                    DestroyAPIView, 
                                    RetrieveUpdateAPIView , 
                                    CreateAPIView, )
from main.order.models import Product, ProductTemplate
from main.api.serializers.reseller.producttemplate import ProductTemplateSerializer,ProductTemplateUCSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin
from main.api.permissions import IsOwner
from main.api.paginations import *

class ProductTemplateListAPIView(ListAPIView):
    #queryset = Product.objects.all()
    serializer_class = ProductTemplateSerializer
    #searchs
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['branch', 'template']
    pagination_class = TemplatePagination
    def get_queryset(self):
        queryset = ProductTemplate.objects.filter(is_deleted=False)
        return queryset
class ProductTemplateDetailAPIView(DestroyModelMixin, RetrieveAPIView, RetrieveUpdateAPIView):
    queryset = ProductTemplate.objects.all()
    serializer_class = ProductTemplateUCSerializer
    lookup_field = 'pk'
    permission_classes = [IsOwner]
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
class ProductTemplateCreateAPIView(CreateAPIView):
    queryset = ProductTemplate.objects.all()
    serializer_class = ProductTemplateUCSerializer
    permission_classes =  [IsAuthenticated]
    #serializer save used , changes
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
