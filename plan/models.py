from django.db import models
from django.conf import settings


class Plan(models.Model):
    name=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    description=models.TextField(max_length=1000)
    count=models.IntegerField(default=0)
    def __str__(self):
        return self.name
    
class PaymentHistory(models.Model):

    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True)
    plan=models.ForeignKey(Plan, on_delete=models.SET_NULL, blank=True, null=True)
    date=models.DateTimeField(auto_now_add=True)
    payment_status=models.BooleanField()
    stock=models.IntegerField(default=0)


    def __str__(self):
        return self.plan.name