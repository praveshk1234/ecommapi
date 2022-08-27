from dataclasses import field, fields
from rest_framework import serializers
from .models import Product,Order
from django.contrib.auth.models import User

class ProductListSerializer(serializers.ModelSerializer):
    category=serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='product-detail',read_only=True,lookup_field='pk')
    class Meta:
        model = Product
        fields = ['id','url','name','price','image','category']
    def get_image(self,obj):
        return obj.image
    def get_category(self,obj):
        return obj.get_category_display()
class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['name','price','image','category','desc','unit']
class ProductDetailSerializer(serializers.ModelSerializer):
    
    order_url = serializers.HyperlinkedIdentityField(view_name="place-order",read_only=True,lookup_field="pk")
    class Meta:
        model=Product
        fields=['id','name','price','image','category','desc','unit','order_url']
  

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password=serializers.CharField(write_only=True,required=True)
    password2=serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username','email','password','password2']
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password":"Password fields didn't match"
            })
        return attrs
    def create(self,validated_data):
        user=User.objects.create(
            username=validated_data['username'],
            email = validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProductOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields= ['name','price']
class OrderSerializer(serializers.ModelSerializer):
    products= ProductOrderSerializer()
    user = serializers.SlugRelatedField(read_only=True,slug_field='username')
    created_at= serializers.DateTimeField(format=" %d/%m/%Y")
    total_price = serializers.SerializerMethodField()
    order_unit=serializers.IntegerField()
    class Meta:
        model = Order
        fields = ['products','user','created_at','order_unit','total_price'] 
    def get_total_price(self,obj):
        prdouct_price = obj.products.price
        return (prdouct_price * obj.order_unit)
   

   
   


