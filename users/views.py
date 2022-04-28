
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm, PostForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .models import Profile, Post, Comment
import random

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('')
    else:
        form = SignupForm()
    return render(request, '', {'form': form})