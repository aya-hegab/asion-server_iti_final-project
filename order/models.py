from django.db import models
from operator import mod 
from django.conf import settings
from users.models import User
from django.contrib.auth.models import AbstractUser
from category.models import *



from product.models import Product
#from django.contrib.auth.models import User
# from users.models import DeliveryMan  # Uncomment this line if needed
#import datetime
#from django.contrib.auth import get_user_model

#UserModel = get_user_model()
class PaymentStatus(models.TextChoices):
    PAID = 'Paid'
    UNPAID = 'Unpaid' 

class PaymentMode(models.TextChoices):
    COD = 'COD'
    CARD = 'CARD' 


class Order(models.Model):
    PENDING_STATE = 'P'
    SHIPPED_STATE = 'S'
    DELIVERED_STATE = 'D'
    CANSCELLED_STATE = 'C'
    READY_STATE = 'R'
    FAILED_STATE = 'F'
    REFUNDED_STATE = 'RF'

    ORDER_STATUS_CHOICES = [
        (PENDING_STATE, "pending"),
        (SHIPPED_STATE, "shipped"),
        (DELIVERED_STATE, "delivered"),
        (CANSCELLED_STATE, "cancelled"),
        (READY_STATE, "ready"),
        (FAILED_STATE, "failed"),
        (REFUNDED_STATE, "refunded"),
    ]
    first_name= models.CharField(max_length=255,default='',blank=False)
    last_name= models.CharField(max_length=255,default='',blank=False)
    email= models.EmailField(max_length=255,default='',blank=False)
    city = models.CharField(max_length=400, default="", blank=False)
    zip_code = models.CharField(max_length=100, default="", blank=False)
    street = models.CharField(max_length=500, default="", blank=False)
    state = models.CharField(max_length=100, default="", blank=False)
    country = models.CharField(max_length=100, default="", blank=False)
    phone_number = models.CharField(max_length=100, default="",blank=False)
    #user = models.ForeignKey(User, related_name="order", on_delete=models.CASCADE)
    #user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    total_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    order_number = models.CharField(max_length=250, blank=True, null=True)
    #delivery_man_id = models.ForeignKey(DeliveryMan,on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=30, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    payment_mode = models.CharField(max_length=30, choices=PaymentMode.choices, default=PaymentMode.COD)
    placed_at= models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=50, choices=ORDER_STATUS_CHOICES, default=PENDING_STATE
    )
    is_paid = models.BooleanField(default=False)
    category= models.ForeignKey(Category,on_delete=models.CASCADE,default=1)


    def __str__(self):
        return str(self.id)
  
class OrderTmp(models.Model):
  PENDING_STATE = 'P'
  SHIPPED_STATE = 'S'
  DELIVERED_STATE = 'D'

  ORDER_STATUS_CHOICES = [
      (PENDING_STATE, "pending"),
      (SHIPPED_STATE, "shipped"),
      (DELIVERED_STATE, "delivered")
  ]
  first_name= models.CharField(max_length=255,default='',blank=False)
  last_name= models.CharField(max_length=255,default='',blank=False)
  email= models.EmailField(max_length=255,default='',blank=False)
  city = models.CharField(max_length=400, default="", blank=False)
  zip_code = models.CharField(max_length=100, default="", blank=False)
  street = models.CharField(max_length=500, default="", blank=False)
  state = models.CharField(max_length=100, default="", blank=False)
  country = models.CharField(max_length=100, default="", blank=False)
  phone_number = models.CharField(max_length=100, default="",blank=False)
  total_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
  order_number = models.CharField(max_length=250, blank=True, null=True)
  payment_status = models.CharField(max_length=30, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
  payment_mode = models.CharField(max_length=30, choices=PaymentMode.choices, default=PaymentMode.COD)
  placed_at= models.DateField(auto_now_add=True)
  status = models.CharField(
        max_length=50, choices=ORDER_STATUS_CHOICES, default=PENDING_STATE
    )
  is_paid = models.BooleanField(default=False)


  def __str__(self):
     return str(self.id)

    





class OrderItemTmp(models.Model):
    order = models.ForeignKey(
        OrderTmp, related_name="orderitems_tmp", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="orderitems_tmp", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200, default="", blank=False)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=False)
    quantity = models.IntegerField()
    SIZE_CHOICES = [
        ('one_size', 'one_size'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
    ]
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.product.name


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="orderitems", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="orderitems", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200, default="", blank=False)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=False)
    quantity = models.IntegerField()
    size = models.CharField(max_length=200, default="", blank=False)
    isReady = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name


