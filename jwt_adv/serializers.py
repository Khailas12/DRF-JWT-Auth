from rest_framework import serializers
from django.contrib.auth import authenticate

from . import models


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True
    )   # cannot be read by client

    # read_only = client wouldn't be able to send a token along with a registration request
    # token = serializers.CharField(max_length=244, read_only=True)

    class Meta:
        model = models.User
        fields = [
            'email',
            'username',
            'password',
            'token'
        ]
        read_only_fields = ('token',)

    def create(self, validated_data):   # creates a new user
        return models.User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=244)
    username = serializers.CharField(max_length=244, read_only=True)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    token = serializers.CharField(max_length=244, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An Email is required to log in'
            )

        if password is None:
            raise serializers.ValidationError(
                'A Password is required to log in'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password not found'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated'
            )

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=123,
        min_length=6,
        write_only=True
    )
    
    class Meta:
        model = models.User
        fields = [
            'email',
            'username',
            'password',
            'token',
        ]
        
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
            
        if password is not None:
            instance.set_password(password)
            
        instance.save()
        return instance
    
