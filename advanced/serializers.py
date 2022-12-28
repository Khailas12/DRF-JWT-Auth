from rest_framework import serializers
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

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


class ChangeUserPasswordSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.User
        fields = [
            'password',
            'password2'
        ]
        
    password = serializers.CharField(
        max_length=100,
        style={'input_type': 'password'},
        write_only=True,
    )
    password2 = serializers.CharField(
        max_length=100,
        style={'input_type': 'password2'},
        write_only=True,
    )

    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        
        if password != password2:
            raise serializers.ValidationError('Password does not match')
        
        # if this is not set then the password would not get changed
        user.set_password(password)
        user.save()
        return attrs



class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    class Meta:
        fields = ['email']
    
    def validate(self, attrs):
        email = attrs.get('email')
        
        if models.User.objects.filter(email=email).exists():
            user = models.User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('uid', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('reset token', token)
            
            link = f'http://localhost:3000/reset/{uid}/{token}'
            print('reset link', link)
            return attrs
        
        else:
            raise ValueError('You are not a registered user')
        

