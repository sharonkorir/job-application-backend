

from rest_framework import serializers
from .models import MpesaPayment,Job
from django.contrib.auth.models import User



class MpesaPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaPayment
        fields = ['id', 'amount', 'contact']

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title','requirements','location', 'jobtype']