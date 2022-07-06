from django.contrib import admin
from .models import Order, OrderItem, Invoice, InvoiceItem, StripeIntent


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',
        'stripe_id',
        'updated_at',
        'created_at',
        'invoice_number',
        'status',
        'user',
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'quantity', 'items')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'invoice_number',
        'transaction_id',
        'payment_method',
        'status',
        'sender_reference',
        'user',
        'updated_at',
        'created_at',
        'discount',
        'vat_amount',
        'net_amount',
        'total',
    )


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit_price', 'quantity')


@admin.register(StripeIntent)
class StripeIntentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'id', 'user', 'status', 'client_secret')
