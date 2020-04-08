from django.urls import path
from .views import product_list, product_detail, product_create, product_update, product_delete

app_name = 'optical'

urlpatterns = [
    path('products/', product_list),
    path('products/create/', product_create),
    # id is the django default id, if model has other pk_name should use it
    # add '/' at the end! without / still work. If don't add '/' at the end, without / doesn't work
    path('products/<id>/', product_detail),
    path('products/<id>/update/', product_update),
    path('products/<id>/delete/', product_delete),
]