from django.urls import path, include
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
)

app_name = 'product'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('<slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('<slug>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('<slug>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]
