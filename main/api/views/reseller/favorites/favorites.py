from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView,RetrieveDestroyAPIView,RetrieveUpdateDestroyAPIView,RetrieveAPIView
from main.order.models import Favorite
from main.api.serializers.reseller.favorites import FavouriteListCreateAPISerializer, FavoriteAPISerializer
from main.api.permissions import IsOwner
from rest_framework.mixins import DestroyModelMixin
class FavouriteListCreateAPIView(ListCreateAPIView): #list & create mixin
    queryset = Favorite.objects.all()
    serializer_class = FavouriteListCreateAPISerializer
    def get_queryset(self):
        return Favorite.objects.filter(user = self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


#silme işleminide beraberinde getiriyor--> RetrieveDestroy
class FavoriteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteAPISerializer
    lookup_field  = 'pk'
    permission_classes = [IsOwner]


#hem getirme hem güncelleme hem silme işlemi--> RetrieveUpdateDestroy


class FavoritesDetailAPIView(DestroyModelMixin,RetrieveAPIView,RetrieveUpdateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteAPISerializer
    lookup_field = 'pk'
    permission_classes = [IsOwner]
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)