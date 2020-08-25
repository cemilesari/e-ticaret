from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (ListAPIView, 
                                    RetrieveAPIView, 
                                    DestroyAPIView, 
                                    RetrieveUpdateAPIView , 
                                    CreateAPIView, )
from main.api.serializers.reseller.categories import CategorySerializer
from main.order.models.category import Category
from rest_framework.permissions import IsAuthenticated
from main.api.paginations import *
from rest_framework.mixins import DestroyModelMixin
class CategoryListAPIView(ListAPIView):
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    pagination_class = CategoryPagination
    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset

class CategoryDetailAPIView(DestroyModelMixin,RetrieveAPIView,RetrieveUpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'
    permission_classes =  [IsAuthenticated]
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
class CategoryCreateAPIView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes =  [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save()
        #serializer.save(user=self.request.user)
