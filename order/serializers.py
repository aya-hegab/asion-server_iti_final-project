from rest_framework import serializers
from .models import *







        

class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"

class OrderItemsTmpSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItemTmp
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    orderItems=serializers.SerializerMethodField(method_name="get_order_items", read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

    def get_order_items(self,obj):
        order_items = obj.orderitems.all()
        serializer = OrderItemsSerializer(order_items,many=True)
        return serializer.data 
    
class OrderTmpSerializer(serializers.ModelSerializer):
    orderItems=serializers.SerializerMethodField(method_name="get_order_items", read_only=True)
    class Meta:
        model = OrderTmp
        fields = '__all__'

    def get_order_items(self,obj):
        order_items = obj.orderitems_tmp.all()
        serializer = OrderItemsTmpSerializer(order_items,many=True)
        return serializer.data 
    

