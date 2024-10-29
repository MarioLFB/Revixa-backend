from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True}
        }


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    
    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("The email field is required.")
        return value
    

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['is_staff'] = user.is_staff

        return token