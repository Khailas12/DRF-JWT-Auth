from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate

from . import serializers


class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = serializers.UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class UserLoginView(APIView):
#     def post(self, request, format=None):
#         serializer = serializers.UserLoginSerializer(data=request.data)
        
#         if serializer.is_valid(raise_exception=True):
#             email = serializer.data.get('email')
#             password = serializer.data.get('password')
#             authenticate(email=email, password=password)
#             return Response({'message': 'User logged in successfully'}, status=status.HTTP_200_OK)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = serializers.UserLoginSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            
            if user is not None:    # user exists
                return Response({'message': 'User logged in successfully'}, status=status.HTTP_200_OK)
            
            else:
                return Response({'errors': {'non_field_errors': [
                    'Email or Password is not valid'
                ]}}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
