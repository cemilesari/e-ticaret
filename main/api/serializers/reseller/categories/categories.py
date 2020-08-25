from rest_framework import serializers
from main.order.models import Category
class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name = 'api:category_detail_view',
        lookup_field = 'pk'
    )

    class Meta:
        model = Category 
        fields = [
            'url',
            'pk',
            'name',
            'created',
        ]
    
