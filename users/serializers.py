from rest_framework import serializers
# from django.contrib.auth.models import User
# from .models import Profile
from .models import User
from django.contrib.auth.password_validation import validate_password as django_validate_password
import re


class UserSerializer(serializers.ModelSerializer):
    # confirmPassword = serializers.CharField()
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name','username', 'email', 'password', 'confirmPassword', 'phone', 'usertype', 'address', 'shopname', 'is_superuser', 'birthdate', 'is_active', 'verification_token']
        extra_kwargs = {
            'password': {'required': True, 'allow_blank': False, 'min_length': 8},
            'confirmPassword': {'required': True, 'allow_blank': False,'min_length': 8 },
            'email': {'required': True, 'allow_blank': False},
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'verification_token': {'read_only': True},
        }

    def validate_shopname(self, value):
        usertype = self.initial_data.get('usertype')
        if usertype == 'vendor' and not value:
            raise serializers.ValidationError("Shop name is required for vendors.")
        elif usertype != 'vendor' and value:
            raise serializers.ValidationError("Shop name is for vendors only.")
        return value

    def validate_password(self, value):
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError("Password must contain at least one uppercase character.")
        if not re.search(r"[!@#$%^&*_]", value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        django_validate_password(value)
        return value

        

    def create(self, validated_data):
     password = validated_data.pop('password', None)
     confirmPassword = validated_data.pop('confirmPassword', None)

    # Ensure that password and confirmPassword are provided
     if password is None or confirmPassword is None:
        raise serializers.ValidationError("Both password and confirmPassword are required.")

    # Ensure that password matches confirmPassword
     if password != confirmPassword:
        raise serializers.ValidationError("Password and confirmPassword do not match.")

     instance = self.Meta.model(**validated_data)

    # Set password using set_password method to hash it
     instance.set_password(password)

     return instance

    

    def update(self, instance, validated_data):
        # Only allow updating certain fields based on user type
        if instance.usertype == 'vendor':
            allowed_fields = ['first_name', 'last_name', 'email', 'address', 'phone', 'shopname']
        else:
            allowed_fields = ['first_name', 'last_name', 'email', 'address', 'phone']

        for field in allowed_fields:
            if field in validated_data:
                setattr(instance, field, validated_data[field])

        instance.save()
        return instance
    
    def validate_phone(self, value):
        if not value.startswith('+20'):
            raise serializers.ValidationError("Mobile number must begin with +20.")
        return value
    
class StatisticsSerializer(serializers.Serializer):
    orders_count = serializers.IntegerField()
    products_count = serializers.IntegerField()
    users_count = serializers.IntegerField()
    

class UserCreationSerializer(serializers.ModelSerializer):
    confirmPassword = serializers.CharField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'confirmPassword', 'phone', 'usertype', 'address', 'shopname', 'is_active', 'is_staff', 'is_superuser', 'birthdate']

    def validate(self, data):
        # Check if password and confirmPassword match
        if data.get('password') != data.get('confirmPassword'):
            raise serializers.ValidationError("Password and confirmPassword do not match.")

        return data

    def create(self, validated_data):
        # Remove confirmPassword from validated data
        validated_data.pop('confirmPassword')
        # Create and return the user object
        return User.objects.create_user(**validated_data)