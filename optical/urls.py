from django.urls import path

from .views import ProductListView, ProductDetailView
from .views import product_create, product_update, product_delete

app_name = 'optical'

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product_list'),
    # path('products/', product_list, name='product_list'),

    path('products/create/', product_create),
    # id is the django default id, if model has other pk_name should use it
    # add '/' at the end! without / still work. If don't add '/' at the end, without / doesn't work

    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    # path('products/<int:id>/', product_detail),

    path('products/<int:id>/update/', product_update),
    path('products/<int:id>/delete/', product_delete),

]
