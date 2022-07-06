from . import views
from django.urls import path


urlpatterns = [
    path('new-address/', views.new_address, name='new-address'),
    path('user-address/', views.user_address, name='user-address'),
    path('set-default/<int:address_id>/', views.set_default, name='set-default'),
    path('edit-address/<int:address_id>/', views.edit_address, name='edit-address'),
    path('del-address/<int:address_id>/', views.del_address, name='del-address'),
    path('account/', views.account, name='account'),
    path('sign-out/', views.logout_view, name='sign-out'),
    path('sign-in/', views.sign_in, name='sign-in'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('verify-email/<int:user_id>/', views.verify_email, name='verify-email'),
    path('orders/', views.orders, name='orders'),
    path('invoices/', views.invoices, name='invoices'),
]
