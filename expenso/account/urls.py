from django.urls import path, re_path

from .views import (
    UserChangeEmailAPIView,
    UserCreateAPIView,
    get_email_token,
    verify_email,
)

app_name = "account"

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register_user"),
    re_path(
        r"(?P<username>[\w.@+-]+)/email-token/$",
        get_email_token,
        name="user_email_token",
    ),
    re_path(
        r"verify-email/(?P<token>[\w.@+-]+)/$",
        verify_email,
        name="verify_email",
    ),
    re_path(
        r"(?P<username>[\w.@+-]+)/change-email/$",
        UserChangeEmailAPIView.as_view(),
        name="change_email",
    ),
]
