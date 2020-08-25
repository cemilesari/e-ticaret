from rest_framework import serializers
from main.order.models import Location
class LocationSerializer(serializers.ModelSerializer):
    detail = serializers.HyperlinkedIdentityField(
        view_name = 'api:location_detail_view',
        lookup_field = 'pk'
    )
    username = serializers.SerializerMethodField()
    class Meta:
        model = Location 
        fields = [
            'detail',
            'pk',
            'user',
            'username',
            'address',
            'city',
            'state',
            'country',
            'zipcode',
            'lati',
            'lngt',
            'mob',
            'tel',
            'fax',
            'url',
            'mail',
            'tax_id',
            'tax_branch',
            'created',
            'is_deleted',
        ]
    def get_username(self, obj):
        return str(obj.user)     
class LocationSerializerDetail(serializers.ModelSerializer):
    detail = serializers.HyperlinkedIdentityField(
        view_name = 'api:location_detail_view',
        lookup_field = 'pk'
    )
    products = serializers.HyperlinkedIdentityField(
        view_name = 'api:product_for_location',
        lookup_field = 'pk'
    )
    username = serializers.SerializerMethodField()
    class Meta:
        model = Location 
        fields = [
            'detail',
            'pk',
            'products',

            'user',
            'username',
            'address',
            'city',
            'state',
            'country',
            'zipcode',
            'lati',
            'lngt',
            'mob',
            'tel',
            'fax',
            'url',
            'mail',
            'tax_id',
            'tax_branch',
            'created',
            'is_deleted',
        ]
    def get_username(self, obj):
        return str(obj.user)  
class LocationUCSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location 
        fields = [
            'pk',
            'address',
            'city',
            'state',
            'country',
            'zipcode',
            'lati',
            'lngt',
            'mob',
            'tel',
            'fax',
            'url',
            'mail',
            'tax_id',
            'tax_branch',
            'created',
            'is_deleted',
        ]
 
