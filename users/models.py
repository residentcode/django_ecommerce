from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, password=None, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        user = self.create_user(email=email, password=password, **other_fields)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email'))

        user = self.model(email=self.normalize_email(email), **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def update_user(self, password=None, **other_fields):
        user = self.model(**other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    verify_code = models.CharField(max_length=255, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Users'
        verbose_name_plural = 'users'

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Address(models.Model):
    user = models.ForeignKey(Users, verbose_name=_('user'), on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address1 = models.CharField(max_length=150)
    address2 = models.CharField(max_length=150, null=True, blank=True)
    zipcode = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=30)
    phone = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    default = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'address'

    def __str__(self):
        return self.full_name

    def set_default(self, user, default=False):
        if default:
            self.user = user
            self.default = True
            self.save()


class AddressItem(models.Model):
    items = models.ForeignKey(Address, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address1 = models.CharField(max_length=150)
    address2 = models.CharField(max_length=150, null=True, blank=True)
    zipcode = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=30)
    phone = models.CharField(max_length=100, null=True, blank=True)
