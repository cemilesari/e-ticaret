from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (ListAPIView, 
                                    RetrieveAPIView, 
                                    DestroyAPIView, 
                                    RetrieveUpdateAPIView , 
                                    CreateAPIView, )
from main.order.models import Location
from main.api.serializers.reseller.locations import LocationSerializer,LocationUCSerializer,LocationSerializerDetail
from rest_framework.permissions import IsAuthenticated
from main.api.permissions import IsOwner
from rest_framework.mixins import DestroyModelMixin
from main.api.paginations import *
from main.api.serializers.reseller.product import ProductSerializer,ProductSerializerHYPER
from main.order.models import Product
class LocationListApiView(ListAPIView):
    serializer_class = LocationSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user', 'city']
    pagination_class = LocationPagination
    def get_queryset(self):
        queryset = Location.objects.filter(is_deleted=False)
        return queryset

class LocationDetailAPIView(DestroyModelMixin,RetrieveAPIView,RetrieveUpdateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializerDetail
    lookup_field = 'pk'
    permission_classes = [IsOwner]
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
class LocationCreateAPIView(CreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationUCSerializer
    permission_classes =  [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LocationDetailForProductAPI(ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['branch', 'template']
    pagination_class = ProductPagination
    def get_queryset(self):
        location=Location.objects.all()
        print(location)
        for loc in location:
            queryset = Product.objects.filter(is_deleted=False, branch__location_id=loc.id)
        return queryset

        
       