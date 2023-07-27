from .models import CartItem, Cart
from accounts.models import Customer
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CartItemSerializer, CartSerializer


class CartApiView(APIView):
   def get(self, request):
      if request.user.is_authenticated:
         user = request.user
         try:
            cart = user.cart
         except:
            cart = Cart.objects.create(customer=user)
         
      else:
         try:
            cart = request.session.get('cart')
         except:
            cart = {"customer":None,"cart_items":[]}
            request.session["cart"] = cart
      serializer = CartSerializer(cart)
      return Response(serializer.data)