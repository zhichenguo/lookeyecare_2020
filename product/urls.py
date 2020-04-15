from django.urls import path

from .views import (
    HomeView,
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView
)

# from .views import register_view, login_view, logout_view

app_name = 'product'

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<slug>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<slug>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]
