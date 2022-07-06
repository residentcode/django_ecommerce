#! /usr/bin/env python3.6
# Python 3.6 or newer required.
import json
from django.http import JsonResponse
import stripe
from django_ecommerce.settings import STRIPE_SECRET_KEY, ENDPOINT_SECRET
import sweetify
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# This is your test secret API key.
stripe.api_key = STRIPE_SECRET_KEY

# Replace this endpoint secret with your endpoint's unique secret
# If you are testing with the CLI, find the secret by running 'stripe listen'
# If you are using an endpoint defined with the API or dashboard, look in your webhook settings
# at https://dashboard.stripe.com/webhooks
endpoint_secret = ENDPOINT_SECRET


@require_POST
@csrf_exempt
def webhook_view(request):
    event = None
    payload = request.body

    try:
        event = json.loads(payload)
    except:
        print('⚠️  Webhook error while parsing basic request.' + str(e))
        return JsonResponse({'success': False})
    if endpoint_secret:
        # Only verify the event if there is an endpoint secret defined
        # Otherwise use the basic event deserialized with json
        sig_header = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except stripe.error.SignatureVerificationError as e:
            print('⚠️  Webhook signature verification failed.' + str(e))
            return JsonResponse({'success': False})

    # Handle the event
    if event and event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']  # contains a stripe.PaymentIntent
        sweetify.success(request, 'success', text='Payment successful', timer=3000, timerProgressBar='true')
        print('Payment for {} succeeded'.format(payment_intent['amount']))

        # Then define and call a method to handle the successful payment intent.
        # handle_payment_intent_succeeded(payment_intent)
    elif event['type'] == 'payment_method.attached':
        payment_method = event['data']['object']  # contains a stripe.PaymentMethod
        # Then define and call a method to handle the successful attachment of a PaymentMethod.
        # handle_payment_method_attached(payment_method)
    else:
        # Unexpected event type
        print('Unhandled event type {}'.format(event['type']))

    return JsonResponse({'success': True})
