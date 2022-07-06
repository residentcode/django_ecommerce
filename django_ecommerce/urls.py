from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django_ecommerce.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', include('product.urls')),
    path('', include('users.urls')),
    path('', include('stripe_payment.urls')),
]+ static(MEDIA_URL, document_root=MEDIA_ROOT)
