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

   def delete(self, request):
      if request.user.is_authenticated:
         user = request.user
         user.cart.cart_items.all().delete()
         serializer = CartSerializer(user.cart)
      else:
         try:
            request.session['cart']["cart_items"]=[]
         except KeyError:
            cart = {"customer":None,"cart_items":[]}
            request.session["cart"] = cart
         serializer = CartSerializer(request.session["cart"])
      return Response(serializer.data)

   def put(self, request):
      cart_items = request.data.get('cart_items')
      cart_items={item['product_id']:item['quantity'] for item in cart_items}
      print(cart_items)
      if not cart_items:
         return Response({'error': 'No cart items provided'}, status=status.HTTP_400_BAD_REQUEST)
      if request.user.is_authenticated:
         user = request.user
         user_cart_items=user.cart.cart_items.all()
         print(cart_items.keys())
         for item in user_cart_items:
           
            if str(item.product.id) not in cart_items.keys():
               item.delete()
            else:
               item.quantity=cart_items[str(item.product.id)]
               item.save()
         serializer = CartSerializer(user.cart)

      else:
         try:
            cart = request.session.get('cart')
         except:
            cart = {"customer":None,"cart_items":[]}
            request.session["cart"] = cart
         serializer = CartSerializer(cart)
      return Response(serializer.data) 