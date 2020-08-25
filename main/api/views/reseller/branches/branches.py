from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (ListAPIView, 
                                    RetrieveAPIView, 
                                    DestroyAPIView, 
                                    RetrieveUpdateAPIView , 
                                    CreateAPIView, )
from main.order.models import Branch
from main.api.serializers.reseller.branches import BranchSerializer,BranchUCSerializer
from rest_framework.permissions import IsAuthenticated

from main.api.permissions import IsOwner
from main.api.paginations import *
from rest_framework.mixins import DestroyModelMixin
class BranchListAPIView(ListAPIView):
    #queryset = Product.objects.all()
    serializer_class = BranchSerializer
    #searchs
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['branch', 'template']
    pagination_class = TemplatePagination
    def get_queryset(self):
        queryset = Branch.objects.filter(is_deleted=False)
        return queryset
class BranchDetailAPIView(DestroyModelMixin,RetrieveAPIView,RetrieveUpdateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    lookup_field = 'pk'
    permission_classes = [IsOwner]
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class BranchCreateAPIView(CreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchUCSerializer
    permission_classes =  [IsAuthenticated]
    #serializer save used , changes
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

#favorite detail düzelteceksin !