from django.utils.translation import ugettext as _
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.db.models import Max
from django.conf import settings
from collections import OrderedDict
from rest_framework.serializers import ModelSerializer, Serializer
from main.users.models import User
from django.contrib.auth.password_validation import validate_password
class UserSerializer(serializers.ModelSerializer):
    detail = serializers.HyperlinkedIdentityField(
        view_name = 'api:user-detail-view',
        lookup_field = 'pk'
    )
    class Meta:
        model = User
        fields = [
            'detail',
            'email',
            'full_name',
            'is_staff',
            'is_active',
            'username',
            'role',
            'lati',
            'lngt',
        ]
class UserSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type' : 'password'}, write_only=True)
    class Meta: 
        model = User
        fields = ['id', 'username', 'full_name' , 'email','password']

    def validate(self, attr):
        validate_password(attr["password"])
        return attr
    def create(self, validated_data):
        user = User.objects.create(
            full_name = validated_data['full_name'],
            email = validated_data['email'],
            username = validated_data['username'],
            
        )
        user.set_password(validated_data['password'])
        user.save()
        return user 
#chancing password
class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    def validate_new_password(self, value):
        validate_password(value)
        return value


