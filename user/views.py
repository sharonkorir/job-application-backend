from rest_framework import generics, status
from user.api import permissions
from user.models import Advertisements, Token, Employer
from rest_framework.response import Response
from user.api.serializers import UserSerializer, JobseekerSignupSerializer, EmployerSignupSerializer, AdvertisementSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from user.api.permissions import IsJobseekerUser, IsEmployerUser
from user.api.permissions import IsAdminOrReadOnly
from django.http import HttpResponse, Http404,HttpResponseRedirect
from email import message
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from .forms import SignupForm, PostForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms import SignupForm, PostForm, UpdateUserForm, UpdateUserProfileForm
from django.http import HttpResponseRedirect
from .models import Profile, Post, Comment
import random
import json
from django.contrib.auth import get_user_model

from django.http import HttpResponse  
from .mpesa_credentials import MpesaAccessToken, LipaNaMpesaPassword
from .models import MpesaPayment
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from .forms import PaymentForm
import time
from .serializers import MpesaPaymentSerializer,JobseekerSerializer, JobSerializer, SignUpSerializer,UpdateUserProfileSerializer
from .models import *
from decouple import config
import json
import requests
from rest_framework import viewsets
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .token import account_activation_token  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  
from django.contrib.auth import get_user_model
from drf_yasg.views import get_schema_view
User = get_user_model()
# from user.forms import EmployerInformationForm

# Create your views here.

class MpesaPaymentViewSet(viewsets.ModelViewSet):  
      serializer_class = MpesaPaymentSerializer
      queryset = MpesaPayment.objects.all()

class JobViewSet(viewsets.ModelViewSet):  
      serializer_class = JobSerializer
      queryset = Job.objects.all()

class SignUpViewSet(viewsets.ModelViewSet):  
      serializer_class = SignUpSerializer
      queryset = User.objects.all()

class UpdateUserProfileViewSet(viewsets.ModelViewSet):  
      serializer_class = UpdateUserProfileSerializer
      queryset = Profile.objects.all()

<<<<<<< HEAD:user/views.py
class JobseekerSignupView(generics.GenericAPIView):
    serializer_class = JobseekerSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            "message": "account created successfully"
        })


class EmployerSignupView(generics.GenericAPIView):
    serializer_class = EmployerSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            "message": "account created successfully"
        })


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer=self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        token, created=Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'is_jobseeker': user.is_jobseeker,
            'is_employer': user.is_employer
        })


class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)


class JobseekerOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsJobseekerUser]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class EmployerOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsEmployerUser]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


    # def post(request):
    #     user = request.user
    #     if request.method == 'POST':
    #         form = EmployerInformationForm(request.POST, request.FILES)
    #         form.is_valid()
    #         update = form.save(commit=False)
    #         form.employer = user
    #         update.save()
    #     return Response ({
    #         'update': update
    #     })


=======
class JobseekerViewSet(viewsets.ModelViewSet):  
      serializer_class = JobseekerSerializer
      queryset = Jobseeker.objects.all()

from django_daraja.mpesa.core import MpesaClient

def index(request):
    cl = MpesaClient()
    # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    phone_number = '07xxxxxxxx'
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = request.build_absolute_uri(reverse('mpesa_stk_push_callback'))
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)

def stk_push_callback(request):
        data = request.body
        # You can do whatever you want with the notification received from MPESA here.
>>>>>>> daraja:users/views.py

def signup(request):  
    if request.method == 'POST':  
        form = SignupForm(request.POST)  
        if form.is_valid():  
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()  
            # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse('Please confirm your email address to complete the registration')  
    else:  
        form = SignupForm()  
    return render(request, '', {'form': form}) 

def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_text(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!')  


# @login_required(login_url='login')
# def profile(request, username):
#     return render(request, 'profile')
@login_required
def profile(request):

    if request.method == 'POST':
        form = UpdateUserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('dashboard')
    else:
        form = UpdateUserProfileForm()

    return render(request, '', {'form':form})

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


def search_results(request):

    if 'employer' in request.GET and request.GET["employer"]:
        search_term = request.GET.get("employer")
        searched_articles = Employer.search_by_title(search_term)
        message = f"{search_term}"

        return Response (request,{"message":message,"employers": searched_articles})

    else:
        message = "You haven't searched for any employer"
        return Response (request,{"message":message})

class AdvertisementsView(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get_add(self, ad_name):
        try:
            return Advertisements.objects.get(ad_name=ad_name)
        except Advertisements.DoesNotExist:
            return Http404

    def get(self, request, ad_name, format=None):
        add = self.get_add(ad_name)
        serializers = AdvertisementSerializer(add)
        return Response(serializers.data)

    def put(self, request, ad_name, format=None):
        add = self.get_add(ad_name)
        serializers = AdvertisementSerializer(add, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)