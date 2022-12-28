from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


from . import serializers, renderers


# Manual token generation
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


class UserRegistrationView(APIView):
    def post(self, request, format=None):
        renderer_classes = (renderers.UserRenderer, )
        serializer = serializers.UserRegistrationSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)

            return Response({
                'token': token,
                'message': 'User created successfully'
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request, format=None):
        renderer_classes = (renderers.UserRenderer, )
        serializer = serializers.UserLoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)

            if user is not None:    # user exists
                token = get_tokens_for_user(user)
                return Response({
                    'token': token,
                    'message': 'User logged in successfully'
                }, status=status.HTTP_200_OK)

            else:
                return Response({'errors': {'non_field_errors': [
                    'Email or Password is not valid'
                ]}}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    renderer_classes = (renderers.UserRenderer, )
    permission_classes = (IsAuthenticated, )    # permission only for authenticated user

    def get(self, request, format=None):
        serializer = serializers.UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

