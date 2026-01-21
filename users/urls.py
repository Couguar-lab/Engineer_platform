from django.urls import path

from .views import login_view, logout_view, otp_verify_view, profile_view

urlpatterns = [
    path("login/", login_view, name="login"),
    path("otp-verify/", otp_verify_view, name="otp_verify"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
]
