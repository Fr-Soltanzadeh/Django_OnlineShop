from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path("login/", api_views.LoginOrRegisterApiView.as_view(), name="login_api"),
    path(
        "verify_code/",
        api_views.VerifyCodeApiView.as_view(),
        name="verify_code_api",
    ),
    path("profile/", api_views.CustomerApiView.as_view(), name="profile_api"),
    path(
        "refresh_token/",
        api_views.RefreshTokenApiView.as_view(),
        name="refresh_token_api",
    ),
    path(
        "user_address/",
        api_views.CustomerAddressListAPIView.as_view(),
        name="user_addresses_api",
    ),
    path(
        "user_address/<int:pk>",
        api_views.CustomerAddressAPIView.as_view(),
        name="user_address_api",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)

