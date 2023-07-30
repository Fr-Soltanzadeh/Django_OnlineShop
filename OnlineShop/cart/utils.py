from decimal import Decimal


def calculate_grand_price(request):
    cart = request.session['cart']
    request.session['cart']['total_price']=str(sum([Decimal(item['product']['price'])*Decimal(item['quantity']) for item in cart['cart_items']]))
    request.session['cart']['grand_price']=str(sum([Decimal(item['product']['discounted_price'])*Decimal(item['quantity']) for item in cart['cart_items']]))
    request.session.save()