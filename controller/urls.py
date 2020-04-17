from django.urls import path

from .views import HomeView, add_to_cart, remove_from_cart, cart_view, checkout, thankyou

# from .views import register_view, login_view, logout_view

app_name = 'controller'

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('cart/', cart_view, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('thankyou/', thankyou, name='thankyou'),
    path('add_to_cart/<slug:product_slug>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug:cart_item_slug>/', remove_from_cart, name='remove_from_cart'),
]
