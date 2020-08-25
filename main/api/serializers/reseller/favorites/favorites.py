from rest_framework.serializers import ModelSerializer
from main.order.models import Favorite
from rest_framework import serializers
class FavouriteListCreateAPISerializer(ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name= 'api:favorite_detail_view',
    )
    class Meta: 
        model = Favorite
        fields = '__all__'
    def validate(self,attrs):
        queryset = Favorite.objects.filter(product= attrs["product"], user = attrs["user"])
        if queryset.exists():
            raise serializers.ValidationError("Product already added favourites.")
        return attrs


class FavoriteAPISerializer(ModelSerializer):
    class Meta:
        model = Favorite
        fields = [
            'body',
        ]