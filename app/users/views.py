from rest_framework import generics, permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

from .serializers import UserSignupSerializer
from .models import User


class UserSignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]


class UserLoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]


class UserRefreshTokenView(TokenRefreshView):
    pass


class UserLogoutView(TokenBlacklistView):
    pass
