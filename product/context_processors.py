from decimal import Decimal
from product.models import Category, Product
from .cart import Cart


def add_tax(amount):
    return round(amount + (amount * 20 / 100), 2)


def product_and_category(*args):
    product = Product.objects.all()
    category = Category.objects.all()
    return {'product': product, 'category': category}


def get_price(request):
    init_cart = Cart(request)
    total_bill = 0
    total_quantity = 0
    coupon = request.session.get('coupon')
    if coupon:
        discount = Decimal(coupon['discount'])
        code = coupon['code']
    else:
        discount = 0
        code = 'No coupon available'
    for key, value in request.session.get('cart').items():
        total_bill += Decimal(value['price']) * value['quantity']
        total_quantity += value['quantity']
    include_vat = add_tax(total_bill)
    final = include_vat - discount
    return {
        'total_bill': Decimal(include_vat),
        'total_quantity': total_quantity,
        'net_amount': total_bill,
        'discount': discount,
        'tax_amount': include_vat - total_bill,
        'final': final,
        'code': code,
    }
