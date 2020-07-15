from django.urls import path, include
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ContactListView,
)

app_name = 'product'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('contacts/', ContactListView.as_view(), name='contacts_list'),
    # path('<category>/', ProductListView.as_view(), name='product_list_filtered'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('<slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('<slug>/<color_gallery>/', ProductDetailView.as_view(), name='product_detail_color'),
    path('<slug>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('<slug>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]
