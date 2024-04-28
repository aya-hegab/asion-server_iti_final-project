from rest_framework import serializers
from review.models import *



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    
    
    
    
    def update(self, instance, validated_data):
        instance.comment = validated_data.get('comment')
        instance.save()
        return instance
    

    

