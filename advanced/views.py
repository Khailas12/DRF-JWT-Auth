from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView



class UserRegistrationView(APIView):
    def post(self):
        