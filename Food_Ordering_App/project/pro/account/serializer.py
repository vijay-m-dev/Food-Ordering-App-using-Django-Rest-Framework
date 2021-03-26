from rest_framework import  serializers
from .models import User, Location


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','mobile_no','password','user_type')
        extra_kwargs = {'password':{'write_only': True},}
    
    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],email=validated_data['email'],mobile_no=validated_data['mobile_no'],password = validated_data['password'],user_type=validated_data['user_type'])
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','mobile_no','user_type']

class OtpMailSerializer(serializers.Serializer):
    otp = serializers.IntegerField(required=True)

class UpdatePasswordOtpMailSerializer(serializers.Serializer):
    otp = serializers.IntegerField(required=True)
    password = serializers.CharField(min_length=8,required=True)

class LocationSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class LocationSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = ['user']


