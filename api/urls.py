
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (product_create,product_list, product_detail, product_destroy, registeruser, order_summary,place_order)
urlpatterns = [
    path('auth/',obtain_auth_token),
    path('register/',registeruser ,name="register"),
    path('product/<int:pk>/',product_detail,name="product-detail"),
    path('products/', product_list,name="product-list"),
    path('placeorder/<int:pk>/',place_order,name="place-order"),
    path('product/create/',product_create,name="product-create"),
    path('product/<int:pk>/delete/',product_destroy, name="product-delete"),
    path('orderdetail/',order_summary,name="order_summary"),
]