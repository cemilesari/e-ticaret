from rest_framework.serializers import ModelSerializer, SerializerMethodField
from main.order.models import Comment, Product
from rest_framework import serializers
from main.users.models import User

class CommentCreateSerializer(ModelSerializer):
    class Meta: 
        model   = Comment
        fields =  ["user", "product", "content", "parent",]        

    def validate(self, attrs):
        if (attrs["parent"]):
            if attrs["parent"].product != attrs["product"]:
                raise serializers.ValidationError("something went wrong")
        return attrs
#iç içe serializer


class ProductSerializer(ModelSerializer):
    class Meta: 
        model = Product
        fields = '__all__'
class UserSerializer(ModelSerializer):
    class Meta: 
        model = User
        fields = '__all__'
class CommentListSerializer(ModelSerializer):
    replies = SerializerMethodField()
    user    = UserSerializer()
    product = ProductSerializer()
    class Meta: 
        model = Comment
        fields = '__all__'
    #altımda herhangi bir children exist ?
    def get_replies(self, obj):
        if obj.any_children:
            return CommentListSerializer(obj.children(), many=True).data #serialize edilmiş veriyi aldık


class CommentDeleteUpdateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'content'
        ]