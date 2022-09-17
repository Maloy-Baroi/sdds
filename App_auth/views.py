from http.client import HTTPResponse
from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from App_auth.models import *

# Create your views here.
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('App_main:home'))
    return render(request, 'App_auth/login-2.html')


def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        thisUser = User(username=username, email=email)
        thisUser.set_password(password)
        thisUser.save()
        patient_problem_profile = Patient_Tested_Results(user=thisUser)
        patient_problem_profile.save()
        login(request, thisUser)
        return HttpResponseRedirect(reverse('App_main:profile-setup'))
    return render(request, 'App_auth/register-2.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_main:home'))
