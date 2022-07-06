from users.models import Address
from django.http import JsonResponse
from django.shortcuts import redirect
import stripe
from django.contrib import messages
from django_ecommerce.settings import STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY
from product.context_processors import get_price
from stripe_payment.models import StripeIntent
from .models import Invoice, Order, InvoiceItem, OrderItem
import sweetify
from django.contrib.auth.decorators import login_required
from product.models import Product
from django.db.models import F


@login_required
def stripe_payment(request):
    if request.method != 'POST':
        return JsonResponse({'stripeData': STRIPE_PUBLIC_KEY})
    stripe.api_key = STRIPE_SECRET_KEY
    try:
        cart_dict = get_price(request)
        amount = str(cart_dict['total_bill']).replace('.', '')
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='EUR',
            receipt_email=request.user.email,
            automatic_payment_methods={
                'enabled': True,
            },
            # metadata = ({'integration_check': 'accept_a_payment'},)
        )
        client_secret = intent.client_secret

        items = {
            'clientSecret': client_secret,
        }
    except Exception as e:
        messages.info(request, f'error {e}')
        return JsonResponse({'error': str(e)})
    return JsonResponse(items)


def cart_items(request):
    for key, value in request.session.get('cart').items():
        return value


@login_required
def payment_response(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request'})
    user = request.user
    body_len = len(request.GET)
    if body_len == 0:
        return JsonResponse({'error': 'not enough data'})
    data = request.GET

    user_id = request.user.id
    if data['redirect_status'] == 'succeeded':
        get_payment_details = stripe.PaymentIntent.retrieve(data['payment_intent'])
        sweetify.success(request, 'success', text='Payment successful')
        cart_dict = get_price(request)
        user_intent = (
            StripeIntent.objects.create(
                user=user,
                client_secret=data['payment_intent_client_secret'],
                payment_id=data['payment_intent'],
                status='paid',
            )
            if not StripeIntent.objects.filter(payment_id=data['payment_intent']).exists()
            else None
        )
        get_address = Address.objects.filter(user=user, default=True).first()
        if not get_address:
            return JsonResponse({'error': 'Please set default address'})
        invoice = Invoice.objects.create(
            user=user,
            full_name=get_address.full_name,
            email=get_address.email,
            address1=get_address.address1,
            address2=get_address.address2,
            zipcode=get_address.zipcode,
            city=get_address.city,
            country=get_address.country,
            phone=get_address.phone,
            transaction_id=data['payment_intent'],
            payment_method='Credit Card',
            net_amount=cart_dict['net_amount'],
            vat_amount=cart_dict['total_bill'] - cart_dict['net_amount'],
            total=cart_dict['total_bill'],
            discount=cart_dict['discount'],
            status='paid',
        )
        invoice_id = invoice.pk

        for key, val in request.session.get('cart').items():
            invoice_item = InvoiceItem.objects.create(
                items=invoice,
                title=val['title'],
                quantity=val['quantity'],
                unit_price=val['price'],
            )

        order = Order.objects.create(
            user=user,
            invoice_number=invoice,
            stripe_id=data['payment_intent'],
            status='completed',
        )
        order_id = order.pk

        for key, val in request.session.get('cart').items():
            order_item = OrderItem.objects.create(
                items=order,
                product=val['title'],
                price=val['price'],
                quantity=val['quantity'],
            )
            Product.objects.filter(id=val['product_id']).update(quantity=F('quantity') - val['quantity'])
        request.session['coupon'] = None
        request.session['cart'] = {}
        return redirect('orders')
    return JsonResponse({'error': data['redirect_status']})
