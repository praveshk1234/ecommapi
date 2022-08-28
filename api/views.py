from collections import OrderedDict
from unicodedata import category
from urllib import request
from django.shortcuts import render
from .serializers import (OrderSerializer, ProductListSerializer,ProductCreateSerializer, RegisterSerializer,ProductDetailSerializer)
from .models import Product,Order
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser,AllowAny
from django.contrib.auth.models import User
from api.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.response import Response
# Create your views here.
@api_view(['GET'])
def index(request):
    context = {
        "products":"Get all the product list",
        'auth/':"POST/  get token using username and password using body parameter",
        'register/':"Post/ username email password and password2 as parameter",
        "product/<pk>/":" GET/ product-detail ",
        'products/':"product-list",
        'placeorder/<int:pk>/':"place-order  with unit",
        'product/create/':" Create the product",
        'product/<int:pk>/delete/': "DELETE/ product-delete",
        'orderdetail/':" GET/ order_summary",
    }
    return Response(context)
class ProductListAPI(generics.ListCreateAPIView):
    queryset= Product.objects.all()
    serializer_class=ProductListSerializer
    def get_queryset(self,*args,**kwargs):
        qs = super().get_queryset(*args,**kwargs) 
        cat = self.request.query_params.get('category')
        if not cat:
            return qs
        return qs.filter(category=cat)
    def perform_create(self, serializer):
        qs= super().perform_create(serializer)
        return qs
product_list =ProductListAPI.as_view()
class ProductCreateAPI(generics.CreateAPIView):
    queryset=Product.objects.all()
    serializer_class = ProductCreateSerializer
    authentication_classes=[IsAdminUser]
product_create = ProductCreateAPI.as_view()

class UserRegister(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = RegisterSerializer
registeruser = UserRegister.as_view()

class RetrieveProductAPI(generics.RetrieveAPIView):
    queryset=Product.objects.all()
    serializer_class = ProductDetailSerializer
   
    lookup_field = 'pk'
    
    
product_detail = RetrieveProductAPI.as_view()  

class DestroyProductAPI(generics.DestroyAPIView):
    queryset=Product.objects.all()
    serializer_class = ProductListSerializer
    authentication_classes=[IsAdminUser]
    permission_classes=[IsAuthenticated]
    lookup_field = 'pk'
    def perform_destroy(self, instance):
        super().perform_destroy(instance)
product_destroy = DestroyProductAPI.as_view()
@api_view(['GET'])
def order_summary(request):
    order=Order.objects.filter(user=request.user)
    serializer =OrderSerializer(order,many=True)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def place_order(request,pk):
    product = Product.objects.get(id=pk)
    print("prodcut",product)
    user = request.user
    if request.method == "POST":
        order_unit = int(request.POST['order'])
        order,created = Order.objects.get_or_create(user=user,products=product,order_unit= order_unit)
        if created:
            order.order_unit = order_unit
        else:
            order.order_unit += order_unit
        order.save()
        updated_unit = product.unit - order_unit
        product.unit = updated_unit
        product.save()
       
    return Response({"message":"order is placed"})