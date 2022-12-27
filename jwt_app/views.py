
from rest_framework_simplejwt.views import TokenObtainPairView
from . import serializers


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer
    
    
