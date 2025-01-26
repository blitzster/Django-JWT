from django.urls import path
from .views import UserInfoView, UserRegistrationView



urlpatterns = [
    path("user-info/", UserInfoView.as_view(), name="user-info"),
    path('register/', UserRegistrationView.as_view(), name="register-user")
]
