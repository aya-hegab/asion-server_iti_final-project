from django.db import models
from category.models import *
from django.conf import settings
from django.core.exceptions import ValidationError


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=255,default="",blank=False)
    category= models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory= models.ForeignKey(SubCategory,on_delete=models.CASCADE,default=1)
    image = models.ImageField(upload_to='product/images/')
    description = models.TextField(max_length=1000,default="",blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    add_date = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    update_date = models.DateTimeField(auto_now=True,null=True, blank=True)
    brand = models.CharField(max_length=225,default="",blank=False)
    stock=models.IntegerField(default=0)
    checkstock=models.IntegerField(default=0)
    ratings = models.DecimalField(max_digits=3,decimal_places=2,default=0)
    new = models.BooleanField(default=False)
    sale = models.BooleanField(default=False)
    newprice = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sizeable=models.BooleanField(default=False)
    stock_S = models.IntegerField(default=0)
    stock_M = models.IntegerField(default=0)
    stock_L = models.IntegerField(default=0)
    stock_XL = models.IntegerField(default=0)
    subImageOne = models.ImageField(upload_to='product/images/' ,blank=True,null=True  )
    subImageTwo = models.ImageField(upload_to='product/images/' ,blank=True,null=True)
    subImageThree = models.ImageField(upload_to='product/images/',blank=True,null=True )
    subImageFour = models.ImageField(upload_to='product/images/' ,blank=True,null=True)
   

    def clean(self):
        super().clean()
        if self.sale :
            if self.newprice >= self.price:
                 raise ValidationError("New price must be less than the original price if the product is on sale.")
        else:
            self.newprice = self.price  
        
    def save(self, *args, **kwargs):
        if self.sizeable:
            self.stock = sum([getattr(self, f"stock_{size}") for size in ['S', 'M', 'L', 'XL']])
            self.checkstock = sum([getattr(self, f"stock_{size}") for size in ['S', 'M', 'L', 'XL']])
        else:
            self.stock_S=0
            self.stock_L=0
            self.stock_M=0
            self.stock_XL=0
            self.checkstock=self.stock
        
            

        super().save(*args, **kwargs)
        


class Rates(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE,related_name='rates')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    rating = models.IntegerField(default=0)
    createAt = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.rating