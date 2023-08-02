from decimal import Decimal
from .models import CartItem, Cart
from products.models import Product
from django.db import IntegrityError


def calculate_grand_price(request):
    cart = request.session['cart']
    request.session['cart']['total_price']=str(sum([Decimal(item['product']['price'])*Decimal(item['quantity']) for item in cart['cart_items']]))
    request.session['cart']['grand_price']=str(sum([Decimal(item['product']['discounted_price'])*Decimal(item['quantity']) for item in cart['cart_items']]))
    request.session.save()


def add_session_to_user_cart(request):
    try:
        user= request.user
        try:
            cart = user.cart
        except:
            cart = Cart.objects.create(customer=user)
        cart_items =  request.session['cart']['cart_items']
        print(cart_items)
        
        for item in cart_items:
            product=Product.objects.get(id=item['product']['id'])
            try:
               cart_item = CartItem.objects.create(product=product,cart = cart)
               cart_item.quantity=item['quantity']
               cart_item.save()
            except IntegrityError:
               cart_item=CartItem.objects.get(product=product , cart= cart)
               cart_item.quantity=item['quantity']
               cart_item.save()
    except KeyError:
        ...
