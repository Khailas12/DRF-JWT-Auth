from django.urls import path
from . import views



urlpatterns = [
    path('user/', views.UserRetrieveUpdateAPIView.as_view()),
    path('users/', views.RegistrationAPIView.as_view()),
    path('users/login/', views.LoginAPIView.as_view()),
]
