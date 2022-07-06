from django.urls import path
from . import views

urlpatterns = [
    path(
        'product-detail/<slug:category_slug>/<slug:product_slug>/',
        views.product_detail,
        name='product-detail',
    ),
    path('category/<slug:category_slug>/', views.category, name='category'),
    path('cart-add/<int:product_id>/', views.cart_add, name='cart-add'),
    path('cart-detail/', views.cart_detail, name='cart-detail'),
    path('cart-clear/', views.cart_clear, name='cart-clear'),
    path('cart-remove/<int:product_id>/', views.item_remove, name='cart-remove'),
    path('item-decrement/<int:product_id>/', views.item_decrement, name='item-decrement'),
    path('item-increment/<int:product_id>/', views.item_increment, name='item-increment'),
    path('checkout/', views.checkout, name='checkout'),
    # path('coupon/', views.get_coupon, name='coupon'),
]
