

from rest_framework import serializers
from .models import MpesaPayment
from django.contrib.auth.models import User



class MpesaPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaPayment
        fields = ['id', 'amount', 'contact']