from rest_framework import serializers
from main.order.models import ProductTemplate

class ProductTemplateSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name = 'api:product_template_detail',
        lookup_field = 'pk',

    )
    username  = serializers.SerializerMethodField()
    Category  = serializers.SerializerMethodField()
    Company   = serializers.SerializerMethodField()

    class Meta:
        model = ProductTemplate
        fields = [
            'url',
            'pk',
            'name',
            'image',
            'body',
            'left',
            'count',
            'username',
            'Category',
            'Company',
            'original_price',
            'price',
            'currency',
            'status',
            'is_deleted',
        ]
    def get_username(self, obj):
        return str(obj.user.username)     
    def get_Category(self, obj):
        return str(obj.category)
    def get_Company(self,obj):
        return str(obj.company.name)

class ProductTemplateUCSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTemplate
        fields = [
            'pk',
            'name',
            'image',
            'body',
            'left',
            'count',
            'category',
            'company',
            'original_price',
            'price',
            'currency',
            'status',
            'is_deleted',
        ]