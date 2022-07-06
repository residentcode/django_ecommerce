from django.contrib import admin
from .models import Users, Address


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'last_name',
        'first_name',
        'email_verified',
        'is_superuser',
        'is_staff',
        'is_active',
        'updated',
        'created',
    )
    search_fields = ('email', 'first_name', 'last_name')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'full_name',
        'phone',
        'country',
        'city',
        'zipcode',
        'address2',
        'address1',
        'created_at',
        'updated_at',
        'user',
    )
    search_fields = ('full_name', 'email', 'phone', 'country', 'city', 'zipcode', 'address1')
