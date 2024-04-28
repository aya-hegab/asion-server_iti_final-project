from rest_framework import serializers
from .models import *

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model=Plan
        fields = '__all__'


class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model=PaymentHistory
        fields = '__all__'

