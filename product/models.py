from io import BytesIO
from django.db import models
from django.urls import reverse
from PIL import Image
from django.core.files import File
from django_ecommerce.settings import DOMAIN_URL
from django.template.defaultfilters import slugify
from django.utils.html import format_html
from django.utils import timezone


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.slug:
            return reverse('category', kwargs={'category_slug': self.slug})
        return 'No image available specified for category'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True, unique=True)
    description = models.TextField(max_length=1000)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='products/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    in_stock = models.BooleanField(default=True)

    class Meta:
        ordering = ['title']

    def get_absolute_url(self):
        if self.category.slug and self.slug:
            return reverse(
                'product-detail',
                kwargs={'category_slug': self.category.slug, 'product_slug': self.slug},
            )
        return 'No product slug was specified for product or category'

    def __str__(self):
        return self.title

    def get_image(self):
        if self.image:
            return self.image.url
        return 'No image was specified for product'

    def get_thumbnail(self):
        if self.thumbnail:
            return DOMAIN_URL + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return DOMAIN_URL + self.thumbnail.url
            else:
                return 'No thumbnail was specified for product'

    def image_tag(self):
        if self.thumbnail:
            return format_html('<img src="%s" width="60px" height="50px">' % self.thumbnail.url)
        else:
            return 'no image found'

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)
        return thumbnail

    def is_available(self):
        if self.quantity >= 1:
            self.in_stock = True
        else:
            self.in_stock = False
        return self.in_stock

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete()
        if self.thumbnail:
            self.thumbnail.delete()
        super(Product, self).delete(*args, **kwargs)


class Image(models.Model):
    images = models.ForeignKey(
        Product, related_name="images", on_delete=models.PROTECT, blank=True, null=True
    )
    image = models.ImageField(upload_to='products/images', blank=True, null=True)

    def get_images(self):
        if self.image:
            return [self.image.url for _ in self.images]
        return 'No image was specified for product(images)'

    def __str__(self):
        return self.images.title

    def delete(self, *args, **kwargs):
        if self.images:
            self.images.delete()
        if self.image:
            self.image.delete()
        super(Image, self).delete(*args, **kwargs)


class Coupon(models.Model):
    product = models.ForeignKey(Product, related_name="product", on_delete=models.CASCADE)
    code = models.CharField(max_length=20, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.DecimalField(max_digits=20, decimal_places=2)
    active = models.BooleanField(default=False)
    limited = models.IntegerField(default=1)
    used = models.IntegerField(default=0)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return self.code
