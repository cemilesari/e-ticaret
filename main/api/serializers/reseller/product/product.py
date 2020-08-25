from rest_framework import serializers
from main.order.models import Product

class ProductSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name = 'api:product_detail_view',
        lookup_field = 'pk'
    )
    username = serializers.SerializerMethodField()
    Branch_Name = serializers.SerializerMethodField()
    Template_Name = serializers.SerializerMethodField()

    class Meta:
        model = Product 
        fields = '__all__'
            #'url',
            #'pk',
            #'Branch_Name',
            #'Template_Name',
            #'left',
            #'count', 
            #'username',
            #'original_price',
            #'price',
            #'start_time',
            #'end_time',
            #'sold_time',
            #'status',
            #'is_deleted',
            #'created',
            #'modified',
            #'branch-----id field',
            #'template---id field',
        #]
    def get_Template_Name(self, obj):
        return str(obj.template.name)
    def get_Branch_Name(self, obj):
        return str(obj.branch.name)
    def get_username(self, obj):
        return str(obj.user.username)     


    #def update(self, instance, validated_data):
         #instance.title = validated_data.get('title' , instance.title)
         #instance.content = validated_data.get('content' , instance.content)
         #instance.save()
         #return instance 

    #def validate(self, attrs):
    #if attrs["title"] == "cemile"
        #raise serializers.ValidationError("olmaz")
    #return attrs


class ProductUCSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product 
        fields = [
            'pk',
            'branch',
            'template',
            'left',
            'count', 
            'original_price',
            'price',
            'start_time',
            'end_time',
            'sold_time',
            'status',
            'is_deleted',
            'created',
            'modified',
            #'branch-----id field',
            #'template---id field',
        ]
class ProductSerializerHYPER(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product 
        fields = '__all__'