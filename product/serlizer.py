
from rest_framework import serializers
from product.models import *



class ProductsSerlizer(serializers.ModelSerializer):
    rates = serializers.SerializerMethodField(method_name='get_rates',read_only=True)


    class Meta:
        model = Product
        fields='__all__'
       
       
    def get_rates(self,obj):
        rates = obj.rates.all()
        serializer = RateSerializer(rates,many=True)
        return serializer.data

  

    def create(self, validated_data):
         #** means 3aml el validate data k dict
        return Product.objects.create(**validated_data)
    

    def update(self, instance, validated_data):
        instance.name=validated_data['name']
        instance.description=validated_data['description']
        instance.price = validated_data['price']
       
        instance.add_date = validated_data['add_date']
        instance.update_date= validated_data['update_date']
        instance.brand = validated_data['brand']
        instance.stock= validated_data['stock']
        instance.stock_S=validated_data['stock_S']
        instance.stock_M=validated_data['stock_M']
        instance.stock_L=validated_data['stock_L']
        instance.stock_XL=validated_data['stock_XL']        
        instance.ratings=validated_data['ratings']
        instance.new=validated_data['new']
        instance.sale=validated_data['sale']
        instance.sizeable=validated_data['sizeable']
        instance.newprice=validated_data['newprice']
      

        if 'image' in validated_data and validated_data['image'] is not None:
           instance.image = validated_data['image']
        elif 'subImageOne' in validated_data and validated_data['subImageOne'] is not None:
           instance.subImageOne = validated_data['subImageOne']
        elif 'subImageTwo' in validated_data and validated_data['subImageTwo'] is not None:
          instance.subImageTwo = validated_data['subImageTwo']
        elif 'subImageThree' in validated_data and validated_data['subImageThree'] is not None:
          instance.subImageThree = validated_data['subImageThree']
        elif 'subImageFour' in validated_data and validated_data['subImageFour'] is not None:
         instance.subImageFour = validated_data['subImageFour']
     
        instance.save()
        return instance
    
 

    
class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rates
        fields = "__all__"