from . import views
from django.urls import path
from stripe_payment import webhook


urlpatterns = [
    path('stripe-payment/', views.stripe_payment, name='stripe-payment'),
    path('payment-response/', views.payment_response, name='payment-response'),
    path('webhook/', webhook.webhook_view, name='webhook'),
]
