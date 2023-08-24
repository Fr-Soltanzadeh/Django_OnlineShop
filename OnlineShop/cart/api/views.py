from ..models import CartItem, Cart
from products.models import Product
from products.api.serializers import ProductSerializer
from accounts.models import Customer
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CartItemSerializer, CartSerializer
from django.db import IntegrityError
from decimal import Decimal
from cart.utils import calculate_total_price_with_discount
from rest_framework import permissions
from accounts.authentication import LoginAuthentication
from django.contrib import messages


class CartApiView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [LoginAuthentication]

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            try:
                cart = user.cart
            except:
                cart = Cart.objects.create(customer=user)
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        else:
            try:
                cart = request.session["cart"]
            except:
                cart = {
                    "customer": None,
                    "cart_items": [],
                    "total_price_with_discount": "0",
                    "total_price": "0",
                }
                request.session["cart"] = cart
        return Response(cart)

    def delete(self, request):
        if request.user.is_authenticated:
            user = request.user
            user.cart.cart_items.all().delete()
            serializer = CartSerializer(user.cart)
            return Response(serializer.data)
        else:
            try:
                request.session["cart"]["cart_items"] = []
                request.session["cart"]["total_price_with_discount"] = 0
                request.session["cart"]["total_price"] = 0
            except KeyError:
                request.session["cart"] = {
                    "customer": None,
                    "cart_items": [],
                    "total_price_with_discount": "0",
                    "total_price": "0",
                }
            request.session.save()
        return Response(request.session["cart"])

    def put(self, request):
        cart_items = request.data.get("cart_items")
        cart_items = {item["product_id"]: item["quantity"] for item in cart_items}
        if request.user.is_authenticated:
            user = request.user
            user_cart_items = user.cart.cart_items.select_related("product")
            for item in user_cart_items:
                product = item.product
                if str(product.id) not in cart_items.keys():
                    item.delete()
                else:
                    if product.quantity == 0:
                        messages.error(
                            request,
                            f"Sorry, the item {product.title} in your cart is not available now.",
                        )
                        return Response(
                            {
                                "message": f"Sorry, the item {product.title} in your cart is not available now."
                            }
                        )
                    elif product.quantity < int(cart_items[str(product.id)]):
                        messages.error(
                            request,
                            f"There are only {product.quantity} number of {product.title} available now.",
                        )
                        return Response(
                            {
                                "message": f"There are only {product.quantity} number of {product.title} available now."
                            }
                        )
                    item.quantity = cart_items[str(item.product.id)]
                    item.save()
            serializer = CartSerializer(user.cart)
            return Response(serializer.data)
        else:
            try:
                user_cart_items = request.session.get("cart")["cart_items"]
                print(user_cart_items)
                for index, item in enumerate(user_cart_items):
                    if str(item["product"]["id"]) not in cart_items.keys():
                        request.session["cart"]["cart_items"].pop(index)
                    else:
                        product = Product.objects.get(id=item["product"]["id"])
                        if product.quantity == 0:
                            messages.error(
                                request,
                                f"Sorry, the item {product.title} in your cart is not available now.",
                            )
                            return Response(
                                {
                                    "message": f"Sorry, the item {product.title} in your cart is not available now."
                                }
                            )
                        elif product.quantity < int(cart_items[str(product.id)]):
                            messages.error(
                                request,
                                f"There are only {product.quantity} number of {product.title} available now.",
                            )
                            return Response(
                                {
                                    "message": f"There are only {product.quantity} number of {product.title} available now."
                                }
                            )
                        request.session["cart"]["cart_items"][index][
                            "quantity"
                        ] = cart_items[str(item["product"]["id"])]
            except:
                request.session["cart"] = {
                    "customer": None,
                    "cart_items": [],
                    "total_price_with_discount": "0",
                    "total_price": "0",
                }
        request.session.save()
        calculate_total_price_with_discount(request)
        return Response(request.session["cart"])


class AddToCartApiView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [LoginAuthentication]

    def post(self, request):
        product_id = request.data.get("product_id")
        product = Product.objects.get(id=int(product_id))
        if not product.is_active:
            return Response({"message": "Product is not available"})
        if request.user.is_authenticated:
            user = request.user
            try:
                cart_item = CartItem.objects.create(product=product, cart=user.cart)
                cart_item.quantity = 1
                cart_item.save()
            except IntegrityError:
                cart_item = CartItem.objects.get(product=product, cart=user.cart)
                cart_item.quantity += 1
                cart_item.save()
            serializer = CartSerializer(user.cart)
            return Response(serializer.data)
        else:
            product = ProductSerializer(product).data
            product["price"] = str(product["price"])
            product["discounted_price"] = str(product["discounted_price"])
            try:
                item_index = [
                    index
                    for index, x in enumerate(request.session["cart"]["cart_items"])
                    if x["product"]["id"] == product_id
                ][0]
                request.session["cart"]["cart_items"][item_index]["quantity"] += 1
            except (IndexError, KeyError):
                if not request.session.get("cart"):
                    request.session["cart"] = {
                        "customer": None,
                        "cart_items": [],
                        "total_price_with_discount": "0",
                        "total_price": "0",
                    }
                request.session["cart"]["cart_items"].append(
                    {"quantity": 1, "product": product}
                )
            request.session.save()
            calculate_total_price_with_discount(request)
            return Response(request.session["cart"])
