from django.urls import path
from . import views



urlpatterns = [
    path('register/', views.UserRegistrationView.as_view()),
    path('login/', views.UserLoginView.as_view()),
    path('profile/', views.UserProfileView.as_view()),
    path('changepassword/', views.ChangeUserPasswordView.as_view()),
    
]
