from django.urls import path

from .views import HomeView, add_to_cart, remove_from_cart, cart_view

# from .views import register_view, login_view, logout_view

app_name = 'controller'

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('cart/', cart_view, name='cart'),
    path('add_to_cart/<slug:product_slug>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug:product_slug>/', remove_from_cart, name='remove_from_cart'),
]
