from rest_framework import serializers
from . import models


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        )
    class Meta:
        model = models.User
        fields = [
            'email',
            'name',
            'password',
            'password2',
            'tc',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }
        
        
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        
        if password != password2:
            raise serializers.ValidationError('Password does not match')
        return attrs
    
    def create(self, validate_data):
        return models.User.objects.create_user(**validate_data)
    
    

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=244)
    class Meta:
        model = models.User
        fields = [
            'email', 
            'password'
        ]
        

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            'id',
            'email',
            'name',
        ]
    
    