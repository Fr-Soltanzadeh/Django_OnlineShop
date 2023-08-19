from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path("login/", views.LoginOrRegisterApiView.as_view(), name="login_api"),
    path(
        "verify_code/",
        views.VerifyCodeApiView.as_view(),
        name="verify_code_api",
    ),
    path("profile/", views.CustomerApiView.as_view(), name="profile_api"),
    path(
        "refresh_token/",
        views.RefreshTokenApiView.as_view(),
        name="refresh_token_api",
    ),
    path(
        "user_address/",
        views.CustomerAddressListCreateAPIView.as_view(),
        name="user_addresses_api",
    ),
    path(
        "user_address/<int:pk>/",
        views.CustomerAddressDetailAPIView.as_view(),
        name="user_address_api",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
