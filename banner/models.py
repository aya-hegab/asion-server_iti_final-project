from django.db import models

class Banner(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='banners/images', default='static/images/notfound.png')
    description=models.TextField(max_length=255, blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)



    def __str__(self):
        return self.title
    

class Discount(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='discounts/images', default='static/images/notfound.png')
    description = models.TextField(max_length=255, blank=True, null=True)
    sale_percentage = models.IntegerField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title