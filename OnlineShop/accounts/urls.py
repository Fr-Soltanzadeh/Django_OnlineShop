from django.urls import path
from . import views
from . import api_views


urlpatterns = [
    path("login/", views.LoginOrRegisterView.as_view(), name="login"),
    path("verify_code/", views.VerifyCodeView.as_view(), name="verify_code"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("login/api/v1/", api_views.LoginOrRegisterApiView.as_view(), name="login_api"),
    path(
        "verify_code/api/v1/",
        api_views.VerifyCodeApiView.as_view(),
        name="verify_code_api",
    ),
    path("profile/api/v1/", api_views.CustomerApiView.as_view(), name="profile_api"),
    path(
        "refresh_token/api/v1/",
        api_views.RefreshTokenApiView.as_view(),
        name="refresh_token_api",
    ),
    path(
        "user_address/api/v1/",
        api_views.CustomerAddressListAPIView.as_view(),
        name="user_addresses_api",
    ),
    path(
        "user_address/api/v1/<int:pk>",
        api_views.CustomerAddressAPIView.as_view(),
        name="user_address_api",
    ),
]
