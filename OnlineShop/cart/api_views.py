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
            cart = {"customer":None,"cart_items":[], "grand_price":0, "total_price":0}
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
            request.session["cart"] = {"customer":None,"cart_items":[], "grand_price":0, "total_price":0}
         serializer = CartSerializer(request.session["cart"])
      return Response(serializer.data)

   def put(self, request):
      cart_items = request.data.get('cart_items')
      cart_items={item['product_id']:item['quantity'] for item in cart_items}
      if request.user.is_authenticated:
         user = request.user
         user_cart_items=user.cart.cart_items.all()
         for item in user_cart_items:
            if str(item.product.id) not in cart_items.keys():
               item.delete()
            else:
               item.quantity=cart_items[str(item.product.id)]
               item.save()
         serializer = CartSerializer(user.cart)
      else:
         try:
            user_cart_items = request.session.get('cart')['cart_items']
            for i in range(len(user_cart_items)):
               item=user_cart_items[i]
               if str(item['product']["id"]) not in cart_items.keys():
                  request.session["cart"]['cart_items'].pop(i)
               else:
                  request.session["cart"]['cart_items'][i]['quantity']=cart_items[str(item['product']['id'])]
         except:
            request.session["cart"] = {"customer":None,"cart_items":[], "grand_price":0, "total_price":0}
         serializer = CartSerializer(request.session["cart"])
      return Response(serializer.data) 
      def post(self, request):
         cart_items = request.data.get('cart_items')
         cart_items={item['product_id']:item['quantity'] for item in cart_items}
         if request.user.is_authenticated:
            user = request.user
            user_cart_items=user.cart.cart_items.all()
            for item in user_cart_items:
               if str(item.product.id) not in cart_items.keys():
                  item.delete()
               else:
                  item.quantity=cart_items[str(item.product.id)]
                  item.save()
            serializer = CartSerializer(user.cart)
         else:
            try:
               user_cart_items = request.session.get('cart')['cart_items']
               for i in range(len(user_cart_items)):
                  item=user_cart_items[i]
                  if str(item['product']["id"]) not in cart_items.keys():
                     request.session["cart"]['cart_items'].pop(i)
                  else:
                     request.session["cart"]['cart_items'][i]['quantity']=cart_items[str(item['product']['id'])]
            except:
               request.session["cart"] = {"customer":None,"cart_items":[], "grand_price":0, "total_price":0}
            serializer = CartSerializer(request.session["cart"])
         return Response(serializer.data) 