from django.urls import path
from . import views

urlpatterns = [
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("pay/<int:order_id>/", views.OrderPayView.as_view(), name="pay"),
    path("verify_order/", views.VerifyOrderView.as_view(), name="verify_order"),
]
