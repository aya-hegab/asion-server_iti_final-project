from django.db import models
from django.conf import settings
from product.models import Product


class Cart(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True)
  item = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
  quantity = models.IntegerField(default=1)
  SIZE_CHOICES = [
        ('one_size', 'one_size'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
    ]
  size = models.CharField(max_length=10, choices=SIZE_CHOICES, null=True, blank=True)
  def __str__(self):
        return f"{self.id} of {self.item.name}"

  def get_total_item_price(self):
        if self.item.sale: 
            return self.quantity * self.item.newprice
        else:
            return self.quantity * self.item.price
