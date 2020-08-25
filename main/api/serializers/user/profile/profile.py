#nested iç içe serializer 

from rest_framework.serializers import ModelSerializer
from account.models import Profile 

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile 
        fields = ('id','note','twitter')

class UserSerializer(ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        field = ('id','first_name','last_name','profile')

    def update(self, instance, validated_data):
        profile = validated_data.pop('profile')
        profile_serializer = ProfileSerializer(instance=instance.profile, data= profile)
        profile_serializer.is_valid(raise_exeption= True)
        profile_serializer.save()
        return super(UserSerializer, self).update(instance, validated_data)