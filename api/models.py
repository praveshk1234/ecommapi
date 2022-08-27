from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    products= models.ForeignKey('Product',related_name="order_products",on_delete=models.SET_NULL,null=True)
    order_unit = models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)


class Product(models.Model):
    Male='M'
    Female='F'
    cat_choice =[
        (Male,'Male'),
        (Female,'Female')
    ]
    name=models.CharField(max_length=40,blank=True,null=True)
    image=models.ImageField(upload_to="images/",blank=True,null=True)
    desc= models.TextField(blank=True,null=True)
    price= models.IntegerField(blank=True,default=0)
    unit=models.IntegerField(blank=True,default=0)
    category= models.CharField(max_length=6,choices=cat_choice,default=Male)
    def __str__(self) -> str:
        return self.name