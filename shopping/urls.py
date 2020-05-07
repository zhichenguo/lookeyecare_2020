from django.urls import path

from .views import (
    add_to_cart, remove_from_cart, thankyou, add_quantity, minus_quantity,
    CartView, OrderListView, OrderDetailView, PaymentView, CheckoutView, AddCouponView,
    RequestExchangeView, RequestRefundView, request_received
)

# from .views import register_view, login_view, logout_view

app_name = 'shopping'

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('thankyou/', thankyou, name='thankyou'),
    path('add_to_cart/<slug:product_slug>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug:cart_item_slug>/', remove_from_cart, name='remove_from_cart'),
    path('add_quantity/<slug:cart_item_slug>/', add_quantity, name='add_quantity'),
    path('minus_quantity/<slug:cart_item_slug>/', minus_quantity, name='minus_quantity'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/<slug>/', OrderDetailView.as_view(), name='order_detail'),
    path('add_coupon/', AddCouponView.as_view(), name='add_coupon'),
    path('request_exchange/', RequestExchangeView.as_view(), name='request_exchange'),
    path('request_refund/', RequestRefundView.as_view(), name='request_refund'),
    path('request_received/', request_received, name='request_received'),
]
