from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    #website = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()
