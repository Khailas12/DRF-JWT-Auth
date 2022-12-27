from rest_framework import serializers
from . import models



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True
    )   # cannot be read by client
    
    # read_only = client wouldn't be able to send a token along with a registration request
    token = serializers.CharField(max_length=244, read_only=True)
    
    class Meta:
        model = models.User
        fields = [
            'email', 
            'username',
            'password',
            'token'
        ]
        
    def create(self, validated_data):   # creates a new user
        return models.User.objects.create_user(**validated_data)
    
    