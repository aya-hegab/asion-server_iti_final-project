from rest_framework import serializers
from cart.models import *


class CartSerlizer(serializers.ModelSerializer):
    item_image = serializers.ImageField(source='item.image', read_only=True)
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_price = serializers.SerializerMethodField()
    subtotal_price = serializers.SerializerMethodField()
    stock = serializers.IntegerField(source='item.stock', read_only=True)
    stock_S = serializers.IntegerField(source='item.stock_S', read_only=True)
    stock_M = serializers.IntegerField(source='item.stock_M', read_only=True)
    stock_L = serializers.IntegerField(source='item.stock_L', read_only=True)
    stock_XL = serializers.IntegerField(source='item.stock_XL', read_only=True)
    def validate(self, data):
        if data['user'].usertype != 'customer':
            raise serializers.ValidationError({'errmsg':"user isn't a customer"})
        return data
    def get_item_price(self, obj):
        return obj.item.newprice if obj.item.sale else obj.item.price
    def get_subtotal_price(self, obj):
        price = obj.item.newprice if obj.item.sale else obj.item.price
        return obj.quantity * price
    class Meta:
        model = Cart
        fields = '__all__'



    def create(self, validated_data):
        # ** means 3aml el validate data k dict
        return Cart.objects.create(**validated_data)
    