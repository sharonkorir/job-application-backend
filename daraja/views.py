

import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
import os
from .forms import PaymentForm
import time
from .models import *
from decouple import config
import json
import requests

from ..users.mpesa_credentials import MpesaAccessToken, LipaNaMpesaPassword
from .models import MpesaPayment

@login_required
def employerPayment(request):
    current_user = request.user
    if request.method == 'POST':
        mpesa_form = PaymentForm(
            request.POST, request.FILES, instance=request.user)
        if mpesa_form.is_valid():
            access_token = MpesaAccessToken().validated_mpesa_access_token
            stk_push_api_url = config("STK_PUSH_API_URL")
            headers = {
                "Authorization": "Bearer %s" % access_token,
                "Content-Type": "application/json",
            }
            request = {
                "BusinessShortCode": LipaNaMpesaPassword().BusinessShortCode,
                "Password": LipaNaMpesaPassword().decode_password,
                "Timestamp": LipaNaMpesaPassword().payment_time,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": "1",
                "PartyA": request.POST.get('contact'),
                "PartyB": LipaNaMpesaPassword().BusinessShortCode,
                "PhoneNumber": request.POST.get('contact'),
                "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
                "AccountReference": "Jobslux",
                "TransactionDesc": "Testing stk push",
            }
            response = requests.post(
                stk_push_api_url, json=request, headers=headers)

            mpesa_form.save()
            user = User.objects.get(id=current_user.id)
            user.is_verified = True
            user.save()
            time.sleep(10)
            return redirect('employerDash')
    else:
        mpesa_form = PaymentForm(instance=request.user)
    context = {
        'mpesa_form': mpesa_form,
    }
    return render(request, 'employers/paymentform.html', context)
