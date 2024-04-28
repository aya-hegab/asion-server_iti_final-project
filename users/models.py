from django.db import models
from cart.models import Cart
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator,RegexValidator
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import BaseUserManager

class CustomToken(Token):
    expires = models.DateTimeField(null=False, blank=False)

    def save(self, *args, **kwargs):
        # Set expiration time to 1 minute from now
        self.expires = timezone.now() + timedelta(days=1)
        super().save(*args, **kwargs)

    def is_expired(self):
        return self.expires and self.expires < timezone.now()


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('DeliveryMan', 'DeliveryMan'),
        ('Admin', 'Admin'),
    ]

    first_name = models.CharField(max_length=10, validators=[MinLengthValidator(limit_value=3), MaxLengthValidator(limit_value=30)])
    last_name = models.CharField(max_length=10,  validators=[MinLengthValidator(limit_value=3), MaxLengthValidator(limit_value=30)])
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    confirmPassword = models.CharField(max_length=255 )
    username = models.CharField(max_length=25 , default='')
    USERNAME_FIELD = 'email'
    phone = models.CharField(max_length=13, validators=[RegexValidator(regex=r'^\+201\d{9}$', message='Invalid phone number', code='invalid_phone')], blank=True)
    usertype = models.CharField(choices=USER_TYPE_CHOICES)
    address = models.CharField(max_length=100, default='')
    shopname = models.CharField(max_length=100,blank=True,default='')
    birthdate=models.DateField(null=True)
    is_active =  models.BooleanField(default=False, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    objects = CustomUserManager()
    REQUIRED_FIELDS = ['first_name', 'last_name','username']


    @classmethod
    def usersList(self):
        return self.objects.all() 
    
    def save(self, *args, **kwargs):
        # Hash the confirmPassword field and save it as the password
        if self.confirmPassword:
            self.password = make_password(self.confirmPassword)
        super().save(*args, **kwargs)

class PasswordResetOTP(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return self.expires_at < timezone.now()
   