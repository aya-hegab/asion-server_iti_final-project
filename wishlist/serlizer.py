from rest_framework import serializers
from wishlist.models import *


class WishlistSerlizer(serializers.ModelSerializer):
    item_image = serializers.ImageField(source='item.image', read_only=True)
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_price = serializers.DecimalField(source='item.price', read_only=True, max_digits=10, decimal_places=2)
    new = serializers.BooleanField(source='item.new', read_only=True)
    sale = serializers.BooleanField(source='item.sale', read_only=True)
    stock = serializers.IntegerField(source='item.stock', read_only=True)

    def validate(self, data):
        if data['user'].usertype != 'customer':
            raise serializers.ValidationError({'errmsg':"user isn't a customer"})
        return data
    
    class Meta:
        model = Wishlist
        fields = '__all__'



    def create(self, validated_data):
        # ** means 3aml el validate data k dict
        return Wishlist.objects.create(**validated_data)
    