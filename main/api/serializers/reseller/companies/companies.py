from rest_framework import serializers
from main.order.models import Company
from main.api.serializers.reseller.product import ProductSerializer


class CompanySerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    products = serializers.HyperlinkedIdentityField(
        view_name = 'api:product_for_company',
        lookup_field = 'pk'
    )
    class Meta:
        model = Company 
        fields = [
            'pk',
            'products',

            'name',
            'body',
            'logo',
            'username',
            'size',
            'category',
            'location',
            'created',
            'is_deleted',
        ]
    def get_username(self, obj):
        return str(obj.user.username)     

class CompanyViewSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name = 'api:company_detail_view',
        lookup_field = 'pk'
    )
    

    username = serializers.SerializerMethodField()
    Location = serializers.SerializerMethodField()
    class Meta:
        model = Company 
        fields = [
            'url',
            'pk',
            'name',
            'body',
            'logo',
            'user',
            'username',
            'size',
            'category',
            'Location',
            'created',
            'is_deleted',
        ]
    def get_username(self, obj):
        return str(obj.user)     
    def get_Location(self, obj):
        return str(obj.location.address)
    
    
class CompanyUCViewSerializer(serializers.ModelSerializer):
    products = serializers.HyperlinkedIdentityField(
        view_name = 'api:product_for_company',
        lookup_field = 'pk'
        
    )
    class Meta:
        model = Company 
        fields = [
            'pk',
            'products',
            'name',
            'body',
            'logo',
            'size',
            'category',
            'location',
            'created',
            'is_deleted',
        ]
