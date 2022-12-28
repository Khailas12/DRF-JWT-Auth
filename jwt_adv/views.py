from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView

from . import serializers, renderers


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny, ]
    renderer_classes = (renderers.UserJSONRenderer, )
    serializer_class = serializers.RegisterSerializer
    
    def post(self, request):
        user = request.data.get('user', {})
        
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
class LoginAPIView(APIView):
    permission_classes = [AllowAny, ]
    renderer_classes = (renderers.UserJSONRenderer, )
    serializer_class = serializers.LoginSerializer
    
    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    renderer_classes = (renderers.UserJSONRenderer, )
    serializer_class = serializers.UserSerializer
    
    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        
    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
        