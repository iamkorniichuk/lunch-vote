from django.urls import path

from .views import UserSignupView, UserLoginView, UserRefreshTokenView, UserLogoutView


app_name = "users"

urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("refresh_token/", UserRefreshTokenView.as_view(), name="refresh_token"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]
