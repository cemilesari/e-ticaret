from rest_framework import serializers
from main.order.models import Branch
class BranchSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name = 'api:branch_detail_view',
        lookup_field = 'pk'
    )
    User = serializers.SerializerMethodField()
    Location = serializers.SerializerMethodField()
    Company  = serializers.SerializerMethodField()

    class Meta:
        model = Branch 
        fields = [
            'url',
            'pk',
            'name',
            'body',
            'user',
            'User',
            'Location',
            'Company',
            'created',
            'is_deleted',
        ]
    def get_User(self, obj):
        return str(obj.user)     
    def get_Location(self, obj):
        return str(obj.location.address)
    def get_Company(self,obj):
        return str(obj.company.name)
class BranchUCSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch 
        fields = [
            'pk',
            'name',
            'body',
            'location',
            'company',
            'created',
            'is_deleted',
        ]
