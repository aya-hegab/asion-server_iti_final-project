from django.db import models
from product.models import Product
from django.conf import settings
import datetime


class Review(models.Model):
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
  comment= models.CharField(max_length=100)
  date = models.DateField(default=datetime.datetime.today)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True)


  @classmethod
  def review_list(self):
        return self.objects.all()


  @classmethod
  def getReviewById(cls, id):
        return cls.objects.get(id=id)
  

