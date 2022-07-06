from django.db import models
from django_ecommerce.settings import AUTH_USER_MODEL
from product.models import Product
from general import random_num


class StripeIntent(models.Model):
    options = [
        ('paid', 'paid'),
        ('canceled', 'canceled'),
        ('refunded', 'refunded'),
        ('disputed', 'disputed'),
        ('partial refunded', 'partial refunded'),
        ('incomplete', 'incomplete'),
    ]
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='intent', on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=50, unique=True)
    client_secret = models.CharField(max_length=50, unique=True, blank=True, null=True)
    status = models.CharField(choices=options, default='incomplete', max_length=100)

    class Meta:
        verbose_name = 'StripeIntent'
        verbose_name_plural = 'StripeIntent'


class Invoice(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='invoice', on_delete=models.CASCADE)
    invoice_number = models.PositiveIntegerField(default=0)
    full_name = models.CharField(max_length=100, default='')
    email = models.CharField(max_length=100, default='')
    address1 = models.CharField(max_length=150, default='')
    address2 = models.CharField(max_length=150, null=True, blank=True)
    zipcode = models.CharField(max_length=10, default='')
    city = models.CharField(max_length=100, default='')
    country = models.CharField(max_length=30, default='')
    phone = models.CharField(max_length=100, null=True, blank=True)
    sender_reference = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=100, default='Unpaid')
    payment_method = models.CharField(max_length=100, default='Credit Card')
    transaction_id = models.CharField(max_length=200, blank=True, null=True, unique=True)
    net_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    vat_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    discount = models.IntegerField(default=0)
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'invoice'

    def save(self, *args, **kwargs):
        if self.invoice_number is not None:
            max_value = Invoice.objects.all().aggregate(largest=models.Max('invoice_number'))['largest']
            if max_value is not None:
                self.invoice_number = max_value + 1
            else:
                self.invoice_number += 1
        super().save(*args, **kwargs)


class InvoiceItem(models.Model):
    items = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='order', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order', on_delete=models.CASCADE, null=True)
    order_number = models.CharField(max_length=50, default=0, editable=False, unique=True)
    invoice_number = models.ForeignKey(Invoice, related_name='order', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stripe_id = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=50, default='incomplete')

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'order'

    def save(self, *args, **kwargs):
        self.order_number = random_num(20)
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    items = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'OrderItem'
