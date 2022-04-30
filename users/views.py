
from email import message
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .forms import SignupForm, PostForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms import SignupForm, PostForm, UpdateUserForm, UpdateUserProfileForm
from django.http import HttpResponseRedirect
from .models import Profile, Post, Comment
import random
import json
from .mpesa_credentials import MpesaAccessToken, LipaNaMpesaPassword
from .models import MpesaPayment
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required

from .forms import PaymentForm
import time
from .serializers import MpesaPaymentSerializer,JobSerializer
from .models import *
from decouple import config
import json
import requests
from rest_framework import viewsets



# Create your views here.
class MpesaPaymentViewSet(viewsets.ModelViewSet):  
      serializer_class = MpesaPaymentSerializer
      queryset = MpesaPayment.objects.all()

class JobViewSet(viewsets.ModelViewSet):  
      serializer_class = JobSerializer
      queryset = Job.objects.all()


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'register', {'form': form})

@login_required(login_url='login')
def profile(request, username):
    return render(request, 'profile')

def user_profile(request, username):
    user_prof = get_object_or_404(User, username=username)
    if request.user == user_prof:
        return redirect('profile', username=request.user.username)
    params = {
        'user_prof': user_prof,
    }
    return render(request, '', params)

@login_required(login_url='login')
def edit_profile(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            return redirect('profile', user.username)
    else:
        user_form = UpdateUserForm(instance=request.user)
        prof_form = UpdateUserProfileForm(instance=request.user.profile)
    params = {
        'user_form': user_form,
        'prof_form': prof_form
    }
    return render(request, 'profile', params)

def create_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.post = post
            post.user = request.user.profile
            post.save()
            return redirect('', post.id)
    else:
        form = PostForm()
    return render(request, 'post', {'form': form})

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
    return render(request, '', context)
